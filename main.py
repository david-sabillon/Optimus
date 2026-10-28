from datetime import datetime
import time
import requests

# Modulos locales
from calculations import hanking_ashi_bars
from bybit_modules import send_order_to_bybit, is_position_open, send_close_to_bybit
from miscelaneos import send_telegram_notification, write_messages
from parameters_file import *


def activacion(symbols):
    print(f"Iniciando sistema de Trading Optimus")
    while True:
        current_time = datetime.now()
        if current_time.minute == 1 and current_time.second == 10 and current_time.weekday() not in (5, 6):
            for symbol in symbols:

                # Se extrae los parametros segun que simbolo se itera
                parameters_name = "parameters_" + symbol.lower()
                parameters = globals()[parameters_name]()

                # Se realiza comprobacion si el simbolo esta marcado como activo en el json
                if parameters.status == 1:
                    pass
                else:
                    continue

            # Se comprueba si hay una orden abierta
                comprobacion = is_position_open(symbol, parameters.api_key, parameters.api_secret, parameters.url_position)
                # Descarga datos si hay posicion abierta o esta en el ciclo de cuatro horas
                if (comprobacion == "Buy" or comprobacion == "Sell") or current_time.hour in (2, 6, 10, 14, 18, 22):
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

                # Comprobacion cada hora de posiciones abiertas que vayan contra tendencia antes del cierre de la vela
                if current_time.hour in (0, 1, 3, 4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17, 19, 20, 21, 23):
                    if comprobacion == "Buy":
                        if last_h == 0:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA. Vela en desarrollo bajista. Se envia orden de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key, parameters.api_secret, parameters.url,
                                                parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                            continue
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"La posicion continua en tendencia alcista. Se reinicia el ciclo de comprobacion dentro de una hora.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)
                            continue

                    elif comprobacion == "Sell":
                        if last_h == 1:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA. Vela en desarrollo alcista. Se envia orden de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key, parameters.api_secret, parameters.url,
                                                parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                            continue
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"La posicion continua en tendencia bajista. Se reinicia el ciclo de comprobacion dentro de una hora.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)
                            continue

                else:
                    # Comienza la logica condicional para comprobar direccion de posicion abierta o señal de entrada en cuatro horas
                    if comprobacion == "Buy":
                        if penultim_h == 0:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA. Se produce señal de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key, parameters.api_secret, parameters.url, parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA activa y sin cambios. Se mantiene la posicion.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)
                            continue
                    elif comprobacion == "Sell":
                        if penultim_h == 1:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA. Se produce señal de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key, parameters.api_secret, parameters.url, parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA activa y sin cambios. Se mantiene la posicion.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)
                            continue

                    # Si no hay orden abierta, se comprueban las condiciones de entrada
                    else:
                        if last_d == 1 and (antepenultim_h == 0 and penultim_h == 1):
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Condiciones de entrada favorables. Se procede con envio de orden ALCISTA.")
                            print(message)
                            write_messages(message)
                            send_order_to_bybit(symbol, "Buy", parameters.api_key, parameters.api_secret, parameters.qty, parameters.url)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        elif last_d == 0 and (antepenultim_h == 1 and penultim_h == 0):
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Condiciones de entrada favorables. Se procede con envio de orden BAJISTA.")
                            print(message)
                            write_messages(message)
                            send_order_to_bybit(symbol,"Sell", parameters.api_key, parameters.api_secret, parameters.qty, parameters.url)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Sin señales de activacion. Se reinicia el ciclo de comprobacion dentro de cuatro horas.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)
                            continue
                time.sleep(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    activacion(['BTCUSDT', 'TSLAUSDT', 'TSMUSDT', 'INTCUSDT', 'HOODUSDT', 'METAUSDT', 'GOOGLUSDT', 'AMZNUSDT', 'SNDKUSDT',
                'AAPLUSDT', 'PLTRUSDT', 'MSTRUSDT', 'COINUSDT', 'NVDAUSDT', 'CSCOUSDT', 'ORCLUSDT', 'EWYUSDT',
                'BABAUSDT', 'SPYUSDT', 'SOXLUSDT', 'SPCXUSDT', 'NOKIAUSDT', 'HYUNDAIUSDT', 'XAUUSDT', 'CLUSDT'])