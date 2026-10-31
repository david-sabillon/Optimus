from types import SimpleNamespace
import requests
from pathlib import Path
import json
import os
import time
from datetime import datetime, timedelta, timezone


def asset_sentiment(symbol, max_retries=5, wait_time=5):
    """Devuelve la tendencia de ``symbol`` según el sentimiento de Marketaux.

    El token debe estar definido en la variable de entorno
    ``MARKETAUX_API_TOKEN``. Los umbrales son estrictos: 0.30 y -0.30 se
    consideran ``neutro``.
    """
    MARKETAUX_SENTIMENT_URL = "https://api.marketaux.com/v1/news/all"
    api_token = os.getenv("MARKETAUX_API_TOKEN")
    if not api_token:
        raise ValueError("Falta definir la variable de entorno MARKETAUX_API_TOKEN.")

    normalized_symbol = symbol.strip().upper()
    if not normalized_symbol:
        raise ValueError("El símbolo del activo no puede estar vacío.")

    published_after = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime(
        "%Y-%m-%dT%H:%M"
    )

    for attempt in range(max_retries):
        try:
            response = requests.get(
                MARKETAUX_SENTIMENT_URL,
                params={
                    "api_token": api_token,
                    "symbols": normalized_symbol,
                    "filter_entities": "true",
                    "must_have_entities": "true",
                    "published_after": published_after,
                },
                timeout=10,
            )
            if not response.ok:
                raise RuntimeError(f"Marketaux respondió con HTTP {response.status_code}.")

            articles = response.json().get("data", [])
            sentiments = [
                entity["sentiment_score"]
                for article in articles
                for entity in article.get("entities", [])
                if entity.get("symbol", "").upper() == normalized_symbol
                and entity.get("sentiment_score") is not None
            ]
            if not sentiments:
                return "sin_datos"

            sentiment = sum(sentiments) / len(sentiments)

            if sentiment is not None and sentiment > 0.30:
                return f"alcista - {sentiment:.2f}"
            if sentiment is not None and sentiment < -0.30:
                return f"bajista - {sentiment:.2f}"
            return f"neutro - {sentiment:.2f}"
        except (requests.RequestException, RuntimeError) as error:
            if attempt == max_retries - 1:
                raise RuntimeError(
                    f"No se pudo consultar Marketaux después de {max_retries} intentos."
                ) from error
            time.sleep(wait_time)

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
