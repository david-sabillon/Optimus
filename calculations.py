from bybit_modules import get_kline_data
from datetime import datetime, timezone


HISTORICAL_CANDLES = 20


def _heikin_ashi_direction(kline_data, temporalidad):
    """Devuelve la dirección HA de la última y penúltima vela recibida.

    Bybit devuelve cada vela con el formato:
    [timestamp, open, high, low, close, volume, turnover]
    y ordenadas de la más reciente a la más antigua.
    """
    if len(kline_data) < 3:
        raise ValueError("Se necesitan al menos tres velas para calcular Heikin-Ashi.")

    # Se ordenan de antigua a reciente para que cada apertura HA use la vela HA previa.
    candles = sorted(kline_data, key=lambda candle: int(candle[0]))
    heikin_ashi = []

    total_candles = len(candles)

    for index, candle in enumerate(candles, start=1):
        candle_time = datetime.fromtimestamp(int(candle[0]) / 1000, tz=timezone.utc)
        open_price, high_price, low_price, close_price = map(float, candle[1:5])
        ha_close = (open_price + high_price + low_price + close_price) / 4

        if heikin_ashi:
            previous_open, previous_close = heikin_ashi[-1]
            ha_open = (previous_open + previous_close) / 2
        else:
            ha_open = (open_price + close_price) / 2

        heikin_ashi.append((ha_open, ha_close))
        # Solo se imprimen las tres últimas; las anteriores calientan el cálculo HA.
        if index > total_candles - 3:
            print(
                f"{temporalidad.capitalize()} | vela {index - (total_candles - 3)} de 3 | "
                f"fecha UTC={candle_time:%Y-%m-%d %H:%M} | "
                f"OHLC Bybit: O={open_price:.8f}, H={high_price:.8f}, "
                f"L={low_price:.8f}, C={close_price:.8f} | "
                f"Heikin-Ashi: O={ha_open:.8f}, C={ha_close:.8f}"
            )

    last_ha_open, last_ha_close = heikin_ashi[-1]
    penultim_ha_open, penultim_ha_close = heikin_ashi[-2]
    antepenultim_ha_open, antepenultim_ha_close = heikin_ashi[-3]

    def classification(ha_open, ha_close):
        return "Alcista" if ha_close > ha_open else "Bajista"

    print(f"Última vela {temporalidad}: {classification(last_ha_open, last_ha_close)}")
    print(f"Penúltima vela {temporalidad}: {classification(penultim_ha_open, penultim_ha_close)}")
    print(
        f"Antepenúltima vela {temporalidad}: "
        f"{classification(antepenultim_ha_open, antepenultim_ha_close)}"
    )

    return int(last_ha_close > last_ha_open), int(penultim_ha_close > penultim_ha_open), int(antepenultim_ha_close > antepenultim_ha_open),


def hanking_ashi_bars():
    """Clasifica las velas Heikin-Ashi semanal, diaria y horaria.

    Cada valor devuelto es 1 para una vela alcista y 0 para una bajista o doji.
    """
    # La importación local evita la dependencia circular con main.py.
    from main import symbol

    heikin_ashi_semanal = get_kline_data(symbol, interval="W", limit=HISTORICAL_CANDLES)
    heikin_ashi_diaria = get_kline_data(symbol, interval="D", limit=HISTORICAL_CANDLES)
    heikin_ashi_hora = get_kline_data(symbol, interval="60", limit=HISTORICAL_CANDLES)

    last_ashi_semanal, penultim_ashi_semanal, antepenultim_ashi_semanal = _heikin_ashi_direction(heikin_ashi_semanal, "semanal")
    last_ashi_diaria, penultim_ashi_diaria, antepenultim_ashi_diaria = _heikin_ashi_direction(heikin_ashi_diaria, "diaria")
    last_ashi_hora, penultim_ashi_hora, antepenultim_ashi_hora = _heikin_ashi_direction(heikin_ashi_hora, "horaria")

    return (
        last_ashi_semanal,
        last_ashi_diaria,
        last_ashi_hora,
        penultim_ashi_semanal,
        penultim_ashi_diaria,
        penultim_ashi_hora,
        antepenultim_ashi_semanal,
        antepenultim_ashi_diaria,
        antepenultim_ashi_hora,
    )
