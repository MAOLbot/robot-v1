import os
import time
from binance.client import Client

# Claves de Binance desde variables de entorno
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = Client(API_KEY, API_SECRET)

# Parámetros desde variables de entorno
symbol = "XRPUSDT"
buy_price = float(os.getenv("BUY_PRICE", 2.14))    # valor por defecto si no está seteado
sell_price = float(os.getenv("SELL_PRICE", 2.16))  # idem

def get_price():
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def get_balance(asset):
    balance = client.get_asset_balance(asset=asset)
    return float(balance['free'])

while True:
    try:
        price = get_price()
        print(f"Precio actual de XRP: {price}")

        usdt_balance = get_balance("USDT")
        xrp_balance = get_balance("XRP")

        if price <= buy_price and usdt_balance > 1:
            qty = round(usdt_balance / price, 2)
            order = client.order_market_buy(symbol=symbol, quantity=qty)
            print(f"Se compró XRP: {order}")

        elif price >= sell_price and xrp_balance > 1:
            qty = round(xrp_balance, 2)
            order = client.order_market_sell(symbol=symbol, quantity=qty)
            print(f"Se vendió XRP: {order}")

    except Exception as e:
        print("Ocurrió un error:", e)

    time.sleep(60)
