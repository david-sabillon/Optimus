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
    status = parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_xauusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_xauusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_clusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_clusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_tslausdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_tslausdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_aaplusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_aaplusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_amznusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_amznusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_babausdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_babausdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_coinusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_coinusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_cscousdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_cscousdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_ewyusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_ewyusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_googlusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_googlusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_hoodusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_hoodusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_hyundaiusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_hyundaiusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_intcusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_intcusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_metausdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_metausdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_mstrusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_mstrusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_nokiausdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_nokiausdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_nvdausdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_nvdausdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_orclusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_orclusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_pltrusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_pltrusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_sndkusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_sndkusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_soxlusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_soxlusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_spcxusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_spcxusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_spyusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_spyusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])

def parameters_tsmusdt():
    parameter_file = Path(__file__).parent / "json_parameters" / "parameters_tsmusdt.json"

    with parameter_file.open("r", encoding="utf-8") as file:
        parameters = json.load(file)

    return SimpleNamespace(
    symbol = parameters["symbol"],
    crypto = parameters["crypto"],
    status=parameters["status"],
    api_key = parameters["api_key"],
    api_secret = parameters["api_secret"],
    software = parameters["software"],
    qty = parameters["qty"],
    url = parameters["url_demo"],
    url_position = parameters["url_position_demo"],
    tg_bot_token = parameters["bot_token"],
    tg_chat_id = parameters["chat_id"])
