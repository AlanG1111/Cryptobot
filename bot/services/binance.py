import requests

BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"


def get_btc_price() -> float:
    params = {"symbol": "BTCUSDT"}
    response = requests.get(BINANCE_PRICE_URL, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()
    return float(data["price"])
