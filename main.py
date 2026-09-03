from datetime import datetime
from pathlib import Path
import time
import json
import requests


# Modulos locales
from calculations import hanking_ashi_bars
from bybit_modules import send_order_to_bybit, is_position_open, send_close_to_bybit
from miscelaneos import send_telegram_notification, write_messages

PARAMETERS_FILE = Path(__file__).with_name("parameters.json")

with PARAMETERS_FILE.open("r", encoding="utf-8") as file:
    parameters = json.load(file)

symbol = parameters["symbol"]
crypto = parameters["crypto"]
api_key = parameters["api_key"]
api_secret = parameters["api_secret"]
software = parameters["software"]
qty = parameters["qty"]
url = parameters["url"]
url_position = parameters["url_position"]
tg_bot_token = parameters["bot_token"]
tg_chat_id = parameters["chat_id"]

def activacion(symbol):
    print(f"Iniciando sistema de Trading {software}")
    while True:
        current_time = datetime.now()
        if current_time.minute == 0 and current_time.second == 3:

            # Se comprueba si hay una orden abierta
            comprobacion = is_position_open(symbol, api_key, api_secret, url_position)

            # Descarga los datos historicos en las tres temporalidades
            try:
                (
                    last_w, last_d, last_h,
                    penultim_w, penultim_d, penultim_h,
                    antepenultim_w, antepenultim_d, antepenultim_h,
                ) = hanking_ashi_bars(symbol)
            except (ValueError, RuntimeError, requests.RequestException) as error:
                message = (f"{current_time:%Y-%m-%d %H:%M}: no se evaluarán señales de "
                f"{symbol} en este ciclo: {error}")
                print(message)
                write_messages(message)
                time.sleep(2)
                continue

            # Comienza la logica condicional para comprobar direccion de posicion abierta o señal de entrada
            if comprobacion == "Buy":
                if antepenultim_h == 1 and penultim_h == 0:
                    message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Posicion ALCISTA. Se produce señal de salida de la posicion."
                    print(message)
                    write_messages(message)
                    send_close_to_bybit(symbol, api_key, api_secret, url, url_position)
                    send_telegram_notification(message, tg_bot_token, tg_chat_id)
                    time.sleep(2)
                else:
                    message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Posicion ALCISTA activa y sin cambios. Se mantiene la posicion."
                    print(message)
                    time.sleep(2)
                    continue
            elif comprobacion == "Sell":
                if antepenultim_h == 0 and penultim_h == 1:
                    message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Posicion BAJISTA. Se produce señal de salida de la posicion."
                    print(message)
                    write_messages(message)
                    send_close_to_bybit(symbol, api_key, api_secret, url, url_position)
                    send_telegram_notification(message, tg_bot_token, tg_chat_id)
                    time.sleep(2)
                else:
                    message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Posicion BAJISTA activa y sin cambios. Se mantiene la posicion."
                    print(message)
                    write_messages(message)
                    time.sleep(2)
                    continue

            # Si no hay orden abierta, se comprueban las condiciones de entrada
            else:
                if last_w == 1 and last_d == 1 and (antepenultim_h == 0 and penultim_h == 1):
                    message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Condiciones de entrada favorables. Se procede con envio de orden ALCISTA."
                    print(message)
                    write_messages(message)
                    send_order_to_bybit(symbol, "Buy", api_key, api_secret, qty, url)
                    send_telegram_notification(message, tg_bot_token, tg_chat_id)
                    time.sleep(2)
                elif last_w == 0 and last_d == 0 and (antepenultim_h == 1 and penultim_h == 0):
                    message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Condiciones de entrada favorables. Se procede con envio de orden BAJISTA."
                    print(message)
                    write_messages(message)
                    send_order_to_bybit(symbol,"Sell", api_key, api_secret, qty, url)
                    send_telegram_notification(message, tg_bot_token, tg_chat_id)
                    time.sleep(2)
                else:
                    message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Sin señales de activacion. Se reinicia el ciclo de comprobacion dentro de una hora."
                    print(message)
                    time.sleep(2)
                    continue
        time.sleep(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    activacion(symbol)
