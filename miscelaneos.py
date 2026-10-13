from types import SimpleNamespace
import requests
from pathlib import Path
import json

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

def parameters_file():
    parameter_file = Path(__file__).with_name("parameters.json")

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url"],
    url_position = parameters["url_position"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])
