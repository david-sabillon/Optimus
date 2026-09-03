import requests
from pathlib import Path

def send_telegram_notification(message, tg_bot_token, tg_chat_id):
    bot_token = tg_bot_token
    chat_id = tg_chat_id
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        requests.post(url, data={'chat_id': chat_id, 'text': message})
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

def write_messages(messages):
    # 1. Obtenemos la ruta del archivo que se está ejecutando
    current_path = Path(__file__).resolve()

    # 2. Buscamos la carpeta raíz (por ejemplo, la que se llama "Optimus")
    # Caminamos hacia atrás en el árbol de carpetas hasta encontrar "Optimus"
    root_path = next(p for p in current_path.parents if p.name == "Optimus")

    # 3. Creamos la ruta final apuntando a esa raíz
    activity_file = root_path / "activity.log"

    with activity_file.open("a", encoding="utf-8") as file:
        file.write(messages + "\n")