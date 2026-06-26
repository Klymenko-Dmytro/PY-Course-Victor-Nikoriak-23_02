import requests
from dotenv import load_dotenv
import os

load_dotenv()

def send_telegram_message(text):
    """Надсилає текстове повідомлення в Telegram-канал."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    channel_id = os.getenv('TELEGRAM_CHANNEL')
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        'chat_id': channel_id,
        'text': text,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Telegram API помилка: {response.status_code} — {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Помилка надсилання в Telegram: {e}")
        return None