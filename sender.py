
import requests
import config

def send_message(context: config.Customer, text: str):
    token = context.token
    chat_id = context.chat_id

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
       "chat_id": chat_id,
       "text": text,
    }
    resp = requests.get(url, params=params)

    # Throw an exception if Telegram API fails
    resp.raise_for_status()

