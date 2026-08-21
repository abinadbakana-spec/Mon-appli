import os
import threading
import time
from bs4 import BeautifulSoup
from flask import Flask
import requests

# === VOS IDENTIFIANTS TELEGRAM ===
TELEGRAM_TOKEN = "8808908958:AAH221gC5Mpot-40uGxW5DMZPhL14v-8NM8"
CHAT_ID = "1989476178"

URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/25028fcd7126544630b8da0c6e60722b5/#services"

# Mini-serveur Web pour garder Render actif
app = Flask(__name__)


@app.route("/")
def home():
    return "Bot de surveillance actif 24/7 !"


def envoyer_alerte(message):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        res = requests.post(api_url, data={"chat_id": CHAT_ID, "text": message})
        print(f"Statut d'envoi Telegram : {res.status_code}")
    except Exception as e:
        print(f"Erreur d'envoi Telegram : {e}")


def verifier_creneaux():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Alerte si le message "Aucun créneau..." n'est plus présent
        if "Aucun créneau horaire n'est disponible" not in soup.text:
            envoyer_alerte(
                f"🚨 UN CRÉNEAU EST DISPONIBLE !\n\nRéservez vite ici : {URL}"
            )
            return True
        else:
            print("Vérification faite : aucun créneau disponible.")
    except Exception as e:
        print(f"Erreur de vérification : {e}")
    return False


def boucle_surveillance():
    # Message de test au démarrage du bot
    envoyer_alerte(
        "🟢 Le bot de surveillance est officiellement lancé et actif sur Render !"
    )

    while True:
        if verifier_creneaux():
            time.sleep(900)  # Pause de 15 minutes si alerte envoyée
        else:
            time.sleep(180)  # Pause de 3 minutes entre chaque vérification


if __name__ == "__main__":
    # Lancement du scraper dans un thread séparé
    threading.Thread(target=boucle_surveillance, daemon=True).start()

    # Détection du port pour Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)