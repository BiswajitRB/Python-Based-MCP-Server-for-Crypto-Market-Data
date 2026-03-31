import ccxt
import asyncio
from typing import List, Any, Dict
from .utils import logger

class ExchangeError(Exception):
    pass


class ExchangeClient:
    """
    Lightweight wrapper around ccxt for standardized fetch_ticker and fetch_ohlcv.
    Uses blocking ccxt calls via run_in_executor so endpoints are non-blocking.
    """

    def __init__(self):
        self._exchanges: Dict[str, ccxt.Exchange] = {}

    def _get_exchange(self, name: str):
        key = name.lower()
        if key in self._exchanges:
            return self._exchanges[key]
        try:
            ex_cls = getattr(ccxt, key)
        except AttributeError:
            raise ExchangeError(f'Unknown exchange: {name}')
        try:
            ex = ex_cls({'enableRateLimit': True})
            # If exchange needs verbose or API keys, add them here or via config
            self._exchanges[key] = ex
            return ex
        except Exception as e:
            logger.exception("Failed to instantiate exchange %s", name)
            raise ExchangeError(str(e))

    async def fetch_ticker(self, exchange: str, symbol: str) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        ex = self._get_exchange(exchange)
        try:
            # run blocking network call in executor
            raw = await loop.run_in_executor(None, lambda: ex.fetch_ticker(symbol))
            # normalize fields for response
            return {
                'exchange': exchange,
                'symbol': symbol,
                'timestamp': raw.get('timestamp'),
                'datetime': raw.get('datetime'),
                'bid': raw.get('bid'),
                'ask': raw.get('ask'),
                'last': raw.get('last'),
                'volume': raw.get('baseVolume') or raw.get('volume'),
                'raw': dict(raw)
            }
        except Exception as e:
            logger.exception("fetch_ticker error for %s %s", exchange, symbol)
            raise ExchangeError(str(e))

    async def fetch_ohlcv(self, exchange: str, symbol: str, since: int = None, limit: int = 100) -> List[List[Any]]:
        loop = asyncio.get_event_loop()
        ex = self._get_exchange(exchange)
        try:
            # ccxt timeframe and since are optional - use 1m by default
            def _call():
                # ccxt expects since in ms or None
                return ex.fetch_ohlcv(symbol, timeframe='1m', since=since, limit=limit)
            data = await loop.run_in_executor(None, _call)
            return data
        except Exception as e:
            logger.exception("fetch_ohlcv error for %s %s", exchange, symbol)
            raise ExchangeError(str(e))

