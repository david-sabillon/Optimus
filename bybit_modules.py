import time
import hashlib
import json
import subprocess
import hmac
import requests
from datetime import datetime


from miscelaneos import write_messages


def get_kline_data(symbol, interval, limit, max_retries=5, wait_time=5):
    """Obtiene velas y reintenta con espera incremental ante límites de Bybit."""
    current_time = datetime.now()
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        'category': 'linear',
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    error_message = f'No se recibió una respuesta válida de Bybit'

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 429:
                error_message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} HTTP 429: Too Many Requests."
                write_messages(error_message)
                print(error_message)
            else:
                response.raise_for_status()
                payload = response.json()
                ret_code = payload.get("retCode")

                if ret_code == 0:
                    return payload.get("result", {}).get("list", [])

                ret_message = payload.get("retMsg", "error desconocido")
                error_message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} {ret_message} (retCode={ret_code})"
                write_messages(error_message)
                print(error_message)
                if ret_code != 10006 and "too many visits" not in ret_message.lower():
                    raise RuntimeError(
                        "Bybit no devolvió velas para "
                        f"{symbol} ({interval}): {ret_message}"
                    )

            if attempt == max_retries - 1:
                break

            delay = wait_time * (attempt + 1)
            message_delay = (
                f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                f"Límite de Bybit al consultar {symbol} ({interval}); "
                f"reintento {attempt + 2}/{max_retries} en {delay} segundos."
            )
            write_messages(message_delay)
            print(message_delay)
            time.sleep(delay)

        except requests.HTTPError as error:
            if error.response is None or error.response.status_code != 429:
                raise
            error_message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} HTTP 429: Too Many Requests"
            write_messages(error_message)
            print(error_message)
            if attempt == max_retries - 1:
                break
            delay = wait_time * (attempt + 1)
            message_delay = (
                f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                f"Límite de Bybit al consultar {symbol} ({interval}); "
                f"reintento {attempt + 2}/{max_retries} en {delay} segundos."
            )
            write_messages(message_delay)
            print(message_delay)
            time.sleep(delay)
        except requests.ConnectionError as error:
            error_message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} error de conexión: {error}"
            write_messages(error_message)
            print(error_message)
            if attempt == max_retries - 1:
                break
            delay = wait_time * (attempt + 1)
            message_connection = (
                f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                f"Error de conexión al consultar {symbol} ({interval}); "
                f"reintento {attempt + 2}/{max_retries} en {delay} segundos."
            )
            write_messages(message_connection)
            print(message_connection)
            time.sleep(delay)
        except requests.Timeout as error:
            error_message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} timeout de conexión: {error}"
            write_messages(error_message)
            print(error_message)
            if attempt == max_retries - 1:
                break
            delay = wait_time * (attempt + 1)
            message_time_out = (
                f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                f"Timeout al consultar {symbol} ({interval}); "
                f"reintento {attempt + 2}/{max_retries} en {delay} segundos."
            )
            write_messages(message_time_out)
            print(message_time_out)
            time.sleep(delay)

    raise RuntimeError(
        f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
        f"Bybit no devolvió velas para {symbol} ({interval}) después de "
        f"{max_retries} intentos: {error_message}"
    )

def send_order_to_bybit(symbol, side, api_key, api_secret, qty, url, max_retries=5, wait_time=5):
    """Envía una orden de mercado al API de Bybit con reintentos en caso de error."""
    current_time = datetime.now()

    for attempt in range(max_retries):
        try:
            timestamp = str(int(time.time() * 1000))  # Tiempo en milisegundos
            recv_window = "5000"

            # Crear el cuerpo de la solicitud para una orden de mercado
            order_data = {
                "category": "linear",
                "symbol": symbol,
                "side": side,  # "Buy" o "Sell"
                "orderType": "Market",  # Orden de mercado
                "qty": str(qty),  # Cantidad
                "timeInForce": "IOC",  # Ejecutar inmediatamente
                "reduceOnly": "false",
                "closeOnTrigger": "false",
            }

            # Serializar el cuerpo de la solicitud
            body_json = json.dumps(order_data, separators=(',', ':'))

            # Generar firma
            payload = f"{timestamp}{api_key}{recv_window}{body_json}"
            signature = hmac.new(
                bytes(api_secret, 'utf-8'),
                bytes(payload, 'utf-8'),
                hashlib.sha256
            ).hexdigest()

            # Configurar headers
            headers = {
                "Content-Type": "application/json",
                "X-BAPI-API-KEY": api_key,
                "X-BAPI-TIMESTAMP": timestamp,
                "X-BAPI-SIGN": signature,
                "X-BAPI-RECV-WINDOW": recv_window,
            }

            # Ejecutar la solicitud usando cURL
            curl_command = [
                "curl", "-X", "POST", url,
                "-H", f"X-BAPI-API-KEY: {api_key}",
                "-H", f"X-BAPI-TIMESTAMP: {timestamp}",
                "-H", f"X-BAPI-SIGN: {signature}",
                "-H", f"X-BAPI-RECV-WINDOW: {recv_window}",
                "-H", "Content-Type: application/json",
                "-d", body_json
            ]

            result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Procesar respuesta
            if result.returncode == 0:
                sent_order = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Orden de mercado enviada exitosamente."
                write_messages(sent_order)
                print(sent_order)
                return True
            else:
                network_error = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Error al enviar la orden (Intento {attempt + 1}/{max_retries})."
                write_messages(network_error)
                print(network_error)
                curl_error = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} {result.stderr}"
                write_messages(curl_error)
                print(curl_error)

        except Exception as e:
            exception_error = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                               f"Error al procesar la orden (Intento {attempt + 1}/{max_retries}): {e}")
            write_messages(exception_error)
            print(exception_error)

        # Esperar antes de reintentar
        time.sleep(wait_time)

    network_error = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                     f"No se pudo enviar la orden después de {max_retries} intentos.")
    write_messages(network_error)
    print(network_error)
    return False

def send_close_to_bybit(symbol, api_key, api_secret, url, url_position, max_retries=5, wait_time=5):
    """
    Cierra una posición abierta en Bybit enviando una orden de mercado en la dirección opuesta.
    Si la API no responde correctamente, reintenta hasta `max_retries` veces con `wait_time` segundos de espera.
    """
    url_position = url_position
    url_order = url
    current_time = datetime.now()

    for attempt in range(max_retries):
        try:
            timestamp = str(int(time.time() * 1000))  # Tiempo en milisegundos
            recv_window = "5000"

            # Obtener información de la posición abierta
            params = {"category": "linear", "symbol": symbol}
            params_query = "&".join(f"{key}={value}" for key, value in params.items())

            payload = f"{timestamp}{api_key}{recv_window}{params_query}"
            signature = hmac.new(
                bytes(api_secret, 'utf-8'),
                bytes(payload, 'utf-8'),
                hashlib.sha256
            ).hexdigest()

            headers = {
                "Content-Type": "application/json",
                "X-BAPI-API-KEY": api_key,
                "X-BAPI-TIMESTAMP": timestamp,
                "X-BAPI-SIGN": signature,
                "X-BAPI-RECV-WINDOW": recv_window,
            }

            response = requests.get(url_position, headers=headers, params=params)

            if response.status_code != 200:
                error_message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Error al obtener posición: {response.text}"
                write_messages(error_message)
                print(error_message)
                time.sleep(wait_time)
                continue

            data = response.json()
            if data.get("retCode") != 0:
                error_api = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Error en la API: {data.get('retMsg')}"
                write_messages(error_api)
                print(error_api)
                time.sleep(wait_time)
                continue

            position = data.get("result", {}).get("list", [])[0]  # Obtener la primera posición
            size = float(position.get("size", 0))
            side = position.get("side")

            if size == 0:
                no_open_position = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} No hay posiciones abiertas para cerrar."
                write_messages(no_open_position)
                print(no_open_position)
                return False

            # Definir la orden opuesta
            close_side = "Sell" if side == "Buy" else "Buy"

            order_data = {
                "category": "linear",
                "symbol": symbol,
                "side": close_side,
                "orderType": "Market",  # Orden de mercado
                "qty": str(size),
                "timeInForce": "IOC"
            }

            body_json = json.dumps(order_data, separators=(',', ':'))

            payload_order = f"{timestamp}{api_key}{recv_window}{body_json}"
            signature_order = hmac.new(
                bytes(api_secret, 'utf-8'),
                bytes(payload_order, 'utf-8'),
                hashlib.sha256
            ).hexdigest()

            headers["X-BAPI-SIGN"] = signature_order  # Actualizar firma

            response_order = requests.post(url_order, headers=headers, data=body_json)

            if response_order.status_code == 200:
                data_order = response_order.json()
                if data_order.get("retCode") == 0:
                    closed_position = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Posición cerrada exitosamente."
                    write_messages(closed_position)
                    print(closed_position)
                    return True
                else:
                    error_api = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Error en la API: {data_order.get('retMsg')}"
                    write_messages(error_api)
                    print(error_api)

            else:
                close_error = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                               f"Error al cerrar la posición (Intento {attempt + 1}/{max_retries}): {response_order.text}")
                write_messages(close_error)
                print(close_error)

        except Exception as e:
            request_error = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                             f"Error al procesar la solicitud (Intento {attempt + 1}/{max_retries}): {e}")
            write_messages(request_error)
            print(request_error)

        time.sleep(wait_time)

    close_error = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                   f"No se pudo cerrar la posición después de {max_retries} intentos.")
    write_messages(close_error)
    print(close_error)
    return False

def is_position_open(symbol, api_key, api_secret, url_position, max_retries=5, wait_time=3):
    """
    Consulta en Bybit si hay una posición abierta para el símbolo dado.
    Devuelve "Buy" o "Sell" si hay posición abierta (size > 0),
    y False en caso contrario.
    """
    url_position = url_position
    current_time = datetime.now()

    for attempt in range(max_retries):
        try:
            timestamp = str(int(time.time() * 1000))
            recv_window = "5000"

            params = {"category": "linear", "symbol": symbol}
            params_query = "&".join(f"{key}={value}" for key, value in params.items())

            payload = f"{timestamp}{api_key}{recv_window}{params_query}"
            signature = hmac.new(
                bytes(api_secret, 'utf-8'),
                bytes(payload, 'utf-8'),
                hashlib.sha256
            ).hexdigest()

            headers = {
                "Content-Type": "application/json",
                "X-BAPI-API-KEY": api_key,
                "X-BAPI-TIMESTAMP": timestamp,
                "X-BAPI-SIGN": signature,
                "X-BAPI-RECV-WINDOW": recv_window,
            }

            response = requests.get(url_position, headers=headers, params=params)

            if response.status_code != 200:
                error_message = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Error al obtener posición: {response.text}"
                write_messages(error_message)
                print(error_message)
                time.sleep(wait_time)
                continue

            data = response.json()
            if data.get("retCode") != 0:
                error_api = f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} Error en la API: {data.get('retMsg')}"
                write_messages(error_api)
                print(error_api)
                time.sleep(wait_time)
                continue

            positions = data.get("result", {}).get("list", [])

            if not positions:
                # No hay posiciones en la lista
                return False

            position = positions[0]
            size = float(position.get("size", 0))

            if size > 0:
                return position.get("side")
            else:
                return False

        except Exception as e:
            position_error = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                              f"Error al consultar la posición (Intento {attempt + 1}/{max_retries}): {e}")
            write_messages(position_error)
            print(position_error)
            time.sleep(wait_time)

    position_error = (f"{current_time.date()} {current_time.hour}:0{current_time.minute}: {symbol} "
                      "No se pudo verificar la posición después de varios intentos.")
    write_messages(position_error)
    print(position_error)
    return False
