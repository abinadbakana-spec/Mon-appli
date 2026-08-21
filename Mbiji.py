import time
import requests
from bs4 import BeautifulSoup

# Configuration
TELEGRAM_TOKEN = "VOTRE_TOKEN_BOT"
CHAT_ID = "VOTRE_CHAT_ID"
URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/25028fcd7126544630b8da0c6e60722b5/#services"


def envoyer_alerte(message):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(api_url, data={"chat_id": CHAT_ID, "text": message})


def verifier_creneaux():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Vérifie la présence du message d'absence de rendez-vous
        if "Aucun créneau horaire n'est disponible" not in soup.text:
            envoyer_alerte(
                f"🚨 UN CRÉNEAU EST DISPONIBLE !\n\nRéservez vite ici : {URL}"
            )
            return True
    except Exception as e:
        print(f"Erreur de vérification: {e}")
    return False


# Boucle de vérification toutes les 3 minutes (180 secondes)
while True:
    if verifier_creneaux():
        # Optionnel: faire une pause plus longue une fois l'alerte envoyée
        time.sleep(900)
    else:
        time.sleep(180)