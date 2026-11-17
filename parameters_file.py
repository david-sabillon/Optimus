from types import SimpleNamespace
import json
from pathlib import Path

# api_key = Valeria
# api_key_prime = Emily

JSON_DIR = Path(__file__).parent / "json_parameters"


def get_parameters(symbol: str) -> SimpleNamespace:
    """Lee los parámetros del JSON correspondiente al símbolo.

    Cada llamada lee el archivo desde disco, permitiendo cambios en caliente
    sin reiniciar el programa.
    """
    parameter_file = JSON_DIR / f"parameters_{symbol.lower()}.json"
    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
        symbol=parameters["symbol"],
        asset=parameters["asset"],
        crypto=parameters["crypto"],
        status=parameters["status"],
        api_key=parameters["api_key"],
        api_secret=parameters["api_secret"],
        api_key_prime=parameters["api_key_prime"],
        api_secret_prime=parameters["api_secret_prime"],
        software=parameters["software"],
        qty=parameters["qty"],
        url=parameters["url_demo"],
        url_position=parameters["url_position_demo"],
        tg_bot_token=parameters["bot_token"],
        tg_chat_id=parameters["chat_id"]
    )

