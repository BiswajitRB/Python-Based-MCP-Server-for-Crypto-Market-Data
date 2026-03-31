# app/services/exchange_service.py

import ccxt

class ExchangeService:
    def __init__(self, exchange_name: str):
        try:
            self.exchange = getattr(ccxt, exchange_name)()
        except AttributeError:
            raise ValueError("Invalid exchange")

    def get_ticker(self, symbol: str):
        return self.exchange.fetch_ticker(symbol)

    def get_ohlcv(self, symbol: str, timeframe="1h", limit=100):
        return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)