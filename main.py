from datetime import datetime
import time
import requests

# Modulos locales
from calculations import hanking_ashi_bars
from bybit_modules import send_order_to_bybit, is_position_open, send_close_to_bybit
from miscelaneos import send_telegram_notification, write_messages, asset_sentiment, thresholds
from parameters_file import *


def activacion(symbols):
    print(f"Iniciando sistema de Trading Optimus")
    while True:
        current_time = datetime.now()
        if current_time.minute == 1 and current_time.second == 10:
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
                comprobacion_prime = is_position_open(symbol, parameters.api_key_prime, parameters.api_secret_prime,
                                                parameters.url_position) # INSTANCIA SECUNDARIA

                # Solo se Descargara datos si hay posicion abierta o esta en el ciclo de cuatro horas
                if ((comprobacion == "Buy" or comprobacion == "Sell") or (comprobacion_prime == "Buy" or comprobacion_prime == "Sell")
                        or current_time.hour in (1, 5, 9, 13, 17, 21)):

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
                if current_time.hour in (0, 2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16, 18, 19, 20, 22, 23):
                    if comprobacion == "Buy":
                        if last_h == 0:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA (Valeria): Vela en desarrollo bajista. Se envia orden de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key, parameters.api_secret, parameters.url,
                                                parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA (Valeria): La posicion continua en tendencia alcista. Se reinicia el ciclo de comprobacion dentro de una hora.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)

                    elif comprobacion == "Sell":
                        if last_h == 1:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA (Valeria): Vela en desarrollo alcista. Se envia orden de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key, parameters.api_secret, parameters.url,
                                                parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA (Valeria): La posicion continua en tendencia bajista. Se reinicia el ciclo de comprobacion dentro de una hora.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)


                    # ---------- Comprobacion de la posicion de la instancia secundaria Prime en 1 hora (Emily) ----------
                    if comprobacion_prime == "Buy":  # INSTANCIA SECUNDARIA
                        if last_h == 1:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA (Emily): Cierre de vela favorable alcista. Se envia orden de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key_prime, parameters.api_secret_prime,
                                                parameters.url,
                                                parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA (Emily): No se presenta vela favorable. Se reinicia el ciclo de comprobacion dentro de una hora.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)
                    elif comprobacion_prime == "Sell":
                        if last_h == 0:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA (Emily): Cierre de vela favorable bajista. Se envia orden de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key_prime, parameters.api_secret_prime,
                                                parameters.url,
                                                parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA (Emily): No se presenta vela favorable. Se reinicia el ciclo de comprobacion dentro de una hora.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)


                else:
                    # Comienza la logica condicional para comprobar direccion de posicion abierta o señal de entrada en CUATRO HORAS
                    if comprobacion == "Buy":
                        if penultim_h == 0:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA (Valeria): Se produce señal de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key, parameters.api_secret, parameters.url, parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA (Valeria): activa y sin cambios. Se mantiene la posicion.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)

                    elif comprobacion == "Sell":
                        if penultim_h == 1:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA (Valeria): Se produce señal de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key, parameters.api_secret, parameters.url, parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA (Valeria): activa y sin cambios. Se mantiene la posicion.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)

                    # -------- Comprobacion para la posicion de la instancia secundaria PRIME en 4 horas (Emily) ---------
                    if comprobacion_prime == "Buy":  # INSTANCIA SECUNDARIA
                        if penultim_h == 1:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA (Emily): Se produce señal de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key_prime, parameters.api_secret_prime,
                                                parameters.url,
                                                parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion ALCISTA (Emily): activa y sin cambios. Se mantiene la posicion.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)
                    elif comprobacion_prime == "Sell":
                        if penultim_h == 0:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA (Emily): Se produce señal de salida de la posicion.")
                            print(message)
                            write_messages(message)
                            send_close_to_bybit(symbol, parameters.api_key_prime, parameters.api_secret_prime,
                                                parameters.url,
                                                parameters.url_position)
                            send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            time.sleep(2)
                        else:
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Posicion BAJISTA (Emily): activa y sin cambios. Se mantiene la posicion.")
                            print(message)
                            write_messages(message)
                            time.sleep(2)


                    # SI NO HAY ORDEN ABIERTA, SE COMPRUEBAN LAS CONDICIONES DE ENTRADA EN CUATRO HORAS
                    else:
                        if last_d == 1 and (antepenultim_h == 0 and penultim_h == 1): # Diario: Alcista, Señal: Alcista
                            # sentiment = asset_sentiment(parameters.asset)
                            high, low = thresholds(symbol, parameters.qty, max_threshold=150)
                            trend_profile = True if current_time.weekday() in (1, 2, 3) else False
                            rage_profile = True if current_time.weekday() in (0, 4, 5, 6) else False

                            if trend_profile:
                                send_order_to_bybit(symbol, "Buy", parameters.api_key, parameters.api_secret, parameters.qty, parameters.url, stoploss=low, takeprofit=high)
                                message = (
                                    f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                    f"Posicion ALCISTA (Valeria): Condiciones de entrada favorables. Se procede con envio de orden.")
                                print(message)
                                write_messages(message)
                                send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                                time.sleep(2)
                            elif rage_profile:  # Emily Profile
                                send_order_to_bybit(symbol, "Sell", parameters.api_key_prime, parameters.api_secret_prime, parameters.qty, parameters.url, stoploss=high, takeprofit=low) # INSTANCIA SECUNDARIA (Emily)
                                message = (
                                    f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                    f"Posicion BAJISTA (Emily): Condiciones de entrada favorables. Se procede con envio de orden.")
                                print(message)
                                write_messages(message)
                                send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                                time.sleep(2)
                        elif last_d == 0 and (antepenultim_h == 1 and penultim_h == 0): # Diario: Bajista, Señal: Bajista
                            # sentiment = asset_sentiment(parameters.asset)
                            high, low = thresholds(symbol, parameters.qty, max_threshold=150)
                            trend_profile = True if current_time.weekday() in (1, 2, 3) else False
                            rage_profile = True if current_time.weekday() in (0, 4, 5, 6) else False

                            if trend_profile:
                                send_order_to_bybit(symbol,"Sell", parameters.api_key, parameters.api_secret, parameters.qty, parameters.url, stoploss=high, takeprofit=low)
                                message = (
                                    f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                    f"Posicion BAJISTA (Valeria): Condiciones de entrada favorables. Se procede con envio de orden.")
                                print(message)
                                write_messages(message)
                                send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                            elif rage_profile:  # Emily Profile
                                send_order_to_bybit(symbol, "Buy", parameters.api_key_prime, parameters.api_secret_prime, parameters.qty, parameters.url, stoploss=low, takeprofit=high) # INSTANCIA SECUNDARIA (Emily)
                                message = (
                                    f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                    f"Posicion ALCISTA (Emily): Condiciones de entrada favorables. Se procede con envio de orden.")
                                print(message)
                                write_messages(message)
                                send_telegram_notification(message, parameters.tg_bot_token, parameters.tg_chat_id)
                                time.sleep(2)
                        else:
                            trend_profile = True if current_time.weekday() in (1, 2, 3) else False
                            perfil = "Valeria" if trend_profile == True else "Emily"
                            message = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                                       f"Sin señales de activacion ({perfil}). Se reinicia el ciclo de comprobacion dentro de cuatro horas.")
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