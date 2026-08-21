import os
import time
import threading
import requests

from flask import Flask
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ============================================================
# CONFIGURATION
# ============================================================

URL = os.environ.get(
    "CITA_URL",
    "https://www.citaconsular.es/es/hosteds/widgetdefault/25028fcd7126544630b8da0c6e60722b5/#services"
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "180"))

# Pour éviter les alertes Telegram répétées
dernier_etat = None


# ============================================================
# SERVEUR FLASK POUR RENDER
# ============================================================

app = Flask(__name__)


@app.route("/")
def home():
    return "🟢 Bot Cita Consular actif."


@app.route("/health")
def health():
    return "OK"


# ============================================================
# TELEGRAM
# ============================================================

def envoyer_alerte(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ TELEGRAM_TOKEN ou CHAT_ID manquant.")
        return False

    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.post(
            api_url,
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "disable_web_page_preview": False
            },
            timeout=15
        )

        print("Telegram :", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return False

        return True

    except Exception as e:
        print("Erreur Telegram :", e)
        return False


# ============================================================
# DETECTION VALIDATION HUMAINE
# ============================================================

def detecter_validation_humaine(page):
    """
    Détecte la présence éventuelle d'une page de validation humaine.

    IMPORTANT :
    Cette fonction ne tente PAS de contourner un CAPTCHA.
    Elle avertit simplement l'utilisateur.
    """

    try:
        texte = page.locator("body").inner_text(timeout=5000).lower()

        mots_validation = [
            "verify you are human",
            "verification",
            "human verification",
            "verify that you are human",
            "captcha",
            "je ne suis pas un robot",
            "vérifiez que vous êtes humain",
            "verifica que eres humano",
            "no soy un robot",
            "verificación humana",
            "security check",
            "checking your browser",
        ]

        for mot in mots_validation:
            if mot in texte:
                return True

        # Recherche de certains iframes généralement utilisés
        # pour des systèmes de vérification.
        frames = page.locator("iframe")

        if frames.count() > 0:
            for i in range(min(frames.count(), 10)):
                try:
                    src = frames.nth(i).get_attribute("src")

                    if src:
                        src = src.lower()

                        indicateurs = [
                            "captcha",
                            "challenge",
                            "turnstile",
                            "recaptcha",
                            "hcaptcha"
                        ]

                        if any(x in src for x in indicateurs):
                            return True

                except Exception:
                    continue

    except Exception as e:
        print("Erreur détection validation :", e)

    return False


# ============================================================
# DETECTION PAGE WELCOME
# ============================================================

def attendre_welcome(page):
    """
    Attend que la page Cita Consular soit chargée.
    """

    print("⏳ Attente de la page Welcome...")

    try:
        page.wait_for_load_state("domcontentloaded", timeout=30000)
    except Exception:
        pass

    # On attend quelques secondes pour laisser le JavaScript travailler
    page.wait_for_timeout(4000)

    try:
        texte = page.locator("body").inner_text(timeout=5000).lower()

        if (
            "welcome" in texte
            or "bienvenido" in texte
            or "bienvenue" in texte
        ):
            print("✅ Page Welcome détectée.")
            return True

    except Exception:
        pass

    return False


# ============================================================
# FERMETURE MESSAGE WELCOME / OK
# ============================================================

def cliquer_ok(page):
    """
    Essaie de fermer une éventuelle boîte de dialogue Welcome.
    """

    textes = [
        "OK",
        "Ok",
        "Aceptar",
        "Accept",
        "Accepter"
    ]

    for texte in textes:
        try:
            bouton = page.get_by_role("button", name=texte, exact=True)

            if bouton.count() > 0 and bouton.first.is_visible():
                print(f"🖱️ Clic sur {texte}")
                bouton.first.click(timeout=3000)
                page.wait_for_timeout(1500)
                return True

        except Exception:
            pass

    # Fallback : recherche de boutons contenant le texte
    try:
        boutons = page.locator("button")

        for i in range(min(boutons.count(), 20)):
            try:
                texte = boutons.nth(i).inner_text().strip().lower()

                if texte in ["ok", "aceptar", "accept", "accepter"]:
                    boutons.nth(i).click(timeout=3000)
                    page.wait_for_timeout(1500)
                    return True

            except Exception:
                continue

    except Exception:
        pass

    return False


# ============================================================
# CLIQUER SUR CONTINUE / CONTINUAR
# ============================================================

def cliquer_continue(page):
    """
    Recherche le bouton Continue / Continuar.
    """

    textes = [
        "Continue",
        "Continuar",
        "CONTINUE",
        "CONTINUAR"
    ]

    for texte in textes:

        try:
            bouton = page.get_by_role(
                "button",
                name=texte,
                exact=True
            )

            if bouton.count() > 0 and bouton.first.is_visible():

                print(f"🖱️ Bouton {texte} trouvé.")

                bouton.first.click(timeout=5000)

                page.wait_for_timeout(3000)

                return True

        except Exception:
            pass

    # Recherche plus large
    try:
        elements = page.locator("text=/Continue|Continuar/i")

        if elements.count() > 0:

            for i in range(min(elements.count(), 10)):

                try:
                    element = elements.nth(i)

                    if element.is_visible():
                        print("🖱️ Continue trouvé par recherche texte.")

                        element.click(timeout=5000)

                        page.wait_for_timeout(3000)

                        return True

                except Exception:
                    continue

    except Exception:
        pass

    return False


# ============================================================
# DETECTION DES CRENEAUX
# ============================================================

def analyser_disponibilite(page):
    """
    Analyse la page réellement rendue par Chromium.

    Cette fonction évite de considérer automatiquement
    une page inconnue comme un créneau disponible.
    """

    try:
        texte = page.locator("body").inner_text(timeout=10000)

    except Exception as e:
        print("Impossible de lire la page :", e)
        return "ERREUR"

    texte_normalise = " ".join(texte.lower().split())

    # --------------------------------------------------------
    # ABSENCE DE CRENEAU
    # --------------------------------------------------------

    mots_absence = [
        "aucun créneau horaire n'est disponible",
        "aucun créneau disponible",
        "no hay citas disponibles",
        "no hay citas disponibles en este momento",
        "no appointments available",
        "no available appointments",
        "sin citas disponibles",
    ]

    for mot in mots_absence:

        if mot in texte_normalise:

            print("❌ Aucun créneau.")

            return "AUCUN_CRENEAU"

    # --------------------------------------------------------
    # INDICES DE DISPONIBILITE
    # --------------------------------------------------------

    mots_disponibilite = [
        "seleccione una fecha",
        "select a date",
        "selecciona una fecha",
        "seleccione hora",
        "select time",
        "disponible",
        "available",
        "disponibilidad"
    ]

    for mot in mots_disponibilite:

        if mot in texte_normalise:

            print("🟢 Indice de disponibilité :", mot)

            return "DISPONIBLE"

    # --------------------------------------------------------
    # CAS INCONNU
    # --------------------------------------------------------

    print("⚠️ Etat inconnu.")
    return "INCONNU"


# ============================================================
# SURVEILLANCE
# ============================================================

def surveiller():

    global dernier_etat

    print("🚀 Démarrage de la surveillance...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )

        context = browser.new_context(
            viewport={
                "width": 1366,
                "height": 768
            },
            locale="fr-FR",
            timezone_id="Europe/Madrid",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        page = context.new_page()

        while True:

            try:

                print("\n==============================")
                print("🔎 Nouvelle vérification")
                print("==============================")

                page.goto(
                    URL,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                page.wait_for_timeout(5000)

                # ------------------------------------------------
                # VALIDATION HUMAINE
                # ------------------------------------------------

                if detecter_validation_humaine(page):

                    print("🚨 VALIDATION HUMAINE DETECTEE")

                    if dernier_etat != "VALIDATION":

                        envoyer_alerte(
                            "⚠️ VALIDATION HUMAINE REQUISE\n\n"
                            "Cita Consular demande une vérification "
                            "humaine avant de continuer.\n\n"
                            f"🔗 {URL}"
                        )

                        dernier_etat = "VALIDATION"

                    # On ne tente PAS de contourner la vérification.
                    time.sleep(CHECK_INTERVAL)
                    continue

                # ------------------------------------------------
                # WELCOME
                # ------------------------------------------------

                attendre_welcome(page)

                cliquer_ok(page)

                # ------------------------------------------------
                # CONTINUE
                # ------------------------------------------------

                if cliquer_continue(page):

                    print("✅ Continue effectué.")

                    page.wait_for_timeout(5000)

                # ------------------------------------------------
                # REVERIFICATION HUMAN CHECK
                # ------------------------------------------------

                if detecter_validation_humaine(page):

                    print("🚨 Validation humaine après Continue.")

                    if dernier_etat != "VALIDATION":

                        envoyer_alerte(
                            "⚠️ VALIDATION HUMAINE REQUISE\n\n"
                            "Une vérification humaine est apparue "
                            "pendant la navigation Cita Consular.\n\n"
                            f"🔗 {URL}"
                        )

                        dernier_etat = "VALIDATION"

                    time.sleep(CHECK_INTERVAL)
                    continue

                # ------------------------------------------------
                # DISPONIBILITE
                # ------------------------------------------------

                etat = analyser_disponibilite(page)

                if etat == "DISPONIBLE":

                    print("🚨 CRENEAU POTENTIELLEMENT DISPONIBLE !")

                    # Anti-spam Telegram
                    if dernier_etat != "DISPONIBLE":

                        envoyer_alerte(
                            "🚨 CRÉNEAU POTENTIELLEMENT DISPONIBLE !\n\n"
                            "La page Cita Consular présente des indices "
                            "de disponibilité.\n\n"
                            "⚡ Vérifiez immédiatement :\n"
                            f"{URL}"
                        )

                    dernier_etat = "DISPONIBLE"

                elif etat == "AUCUN_CRENEAU":

                    print("❌ Aucun créneau.")

                    dernier_etat = "AUCUN_CRENEAU"

                elif etat == "INCONNU":

                    print(
                        "⚠️ Page inconnue : "
                        "aucune alerte de créneau envoyée."
                    )

                    dernier_etat = "INCONNU"

                else:

                    print("⚠️ Erreur pendant l'analyse.")

                # ------------------------------------------------
                # ATTENTE
                # ------------------------------------------------

                time.sleep(CHECK_INTERVAL)

            except PlaywrightTimeoutError:

                print("⏱️ Timeout de la page.")

                time.sleep(60)

            except Exception as e:

                print("❌ Erreur surveillance :", e)

                time.sleep(60)

        browser.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN manquant.")

    if not CHAT_ID:
        print("❌ CHAT_ID manquant.")

    threading.Thread(
        target=surveiller,
        daemon=True
    ).start()

    port = int(os.environ.get("PORT", "10000"))

    app.run(
        host="0.0.0.0",
        port=port
    )