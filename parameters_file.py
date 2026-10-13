from types import SimpleNamespace
import json
from pathlib import Path

def parameters_btcusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_btcusdt.json"

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

def parameters_xauusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_xauusdt.json"

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


def parameters_clusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_clusdt.json"

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