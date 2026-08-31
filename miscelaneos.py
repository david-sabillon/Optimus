import requests

def send_telegram_notification(message, tg_bot_token, tg_chat_id):
    bot_token = tg_bot_token
    chat_id = tg_chat_id
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        requests.post(url, data={'chat_id': chat_id, 'text': message})
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")