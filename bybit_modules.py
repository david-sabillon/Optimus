import time
import hashlib
import json
import subprocess
import hmac
import requests
from colorama import Fore


def get_kline_data(symbol, interval, limit):
    """Obtiene datos del API de Bybit."""
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        'category': 'linear',
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('result', {}).get('list', [])

def send_order_to_bybit(symbol, side, api_key, api_secret, qty, url, max_retries=5, wait_time=2):
    """Envía una orden de mercado al API de Bybit con reintentos en caso de error."""

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
                print(Fore.GREEN + "Orden de mercado enviada exitosamente." + Fore.RESET)
                return True
            else:
                print(Fore.RED + f"Error al enviar la orden (Intento {attempt + 1}/{max_retries})." + Fore.RESET)
                print(Fore.RED + result.stderr + Fore.RESET)

        except Exception as e:
            print(Fore.RED + f"Error al procesar la orden (Intento {attempt + 1}/{max_retries}): {e}" + Fore.RESET)

        # Esperar antes de reintentar
        time.sleep(wait_time)

    print(Fore.RED + f"No se pudo enviar la orden después de {max_retries} intentos." + Fore.RESET)
    return False

def send_close_to_bybit(symbol, api_key, api_secret, url, url_position, max_retries=5, wait_time=2):
    """
    Cierra una posición abierta en Bybit enviando una orden de mercado en la dirección opuesta.
    Si la API no responde correctamente, reintenta hasta `max_retries` veces con `wait_time` segundos de espera.
    """
    url_position = url_position
    url_order = url


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
                print(Fore.RED + f"Error al obtener posición: {response.text}" + Fore.RESET)
                time.sleep(wait_time)
                continue

            data = response.json()
            if data.get("retCode") != 0:
                print(Fore.RED + f"Error en la API: {data.get('retMsg')}" + Fore.RESET)
                time.sleep(wait_time)
                continue

            position = data.get("result", {}).get("list", [])[0]  # Obtener la primera posición
            size = float(position.get("size", 0))
            side = position.get("side")

            if size == 0:
                print(Fore.YELLOW + "No hay posiciones abiertas para cerrar." + Fore.RESET)
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
                    print(Fore.GREEN + "Posición cerrada exitosamente." + Fore.RESET)
                    return True
                else:
                    print(Fore.RED + f"Error en la API: {data_order.get('retMsg')}" + Fore.RESET)

            else:
                print(
                    Fore.RED + f"Error al cerrar la posición (Intento {attempt + 1}/{max_retries}): {response_order.text}" + Fore.RESET)

        except Exception as e:
            print(Fore.RED + f"Error al procesar la solicitud (Intento {attempt + 1}/{max_retries}): {e}" + Fore.RESET)

        time.sleep(wait_time)

    print(Fore.RED + f"No se pudo cerrar la posición después de {max_retries} intentos." + Fore.RESET)
    return False

def is_position_open(symbol, api_key, api_secret, url_position, max_retries=5, wait_time=2):
    """
    Consulta en Bybit si hay una posición abierta para el símbolo dado.
    Devuelve "Buy" o "Sell" si hay posición abierta (size > 0),
    y False en caso contrario.
    """
    url_position = url_position

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
                print(f"Error al obtener posición: {response.text}")
                time.sleep(wait_time)
                continue

            data = response.json()
            if data.get("retCode") != 0:
                print(f"Error en la API: {data.get('retMsg')}")
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
            print(f"Error al consultar la posición (Intento {attempt + 1}/{max_retries}): {e}")
            time.sleep(wait_time)

    print("No se pudo verificar la posición después de varios intentos.")
    return False
