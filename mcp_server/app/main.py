from fastapi import FastAPI, HTTPException, Request, Path
from fastapi.responses import StreamingResponse
import asyncio
from .exchange_client import ExchangeClient, ExchangeError
from .cache import ttl_cache
from .schemas import TickerResponse, OHLCVResponse
from .utils import logger, safe_str

app = FastAPI(title='MCP - Market Connector Proxy', version='0.1.0')
client = ExchangeClient()


@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.get('/ticker/{exchange}/{symbol:path}', response_model=TickerResponse)
async def get_ticker(exchange: str, symbol: str = Path(..., description="Market symbol, e.g. BTC/USDT")):
    """
    symbol supports slashes (use path converter), e.g. BTC/USDT
    """
    try:
        key = f"ticker:{exchange}:{symbol}"
        #data = await ttl_cache.get_or_set(key, lambda: client.fetch_ticker(exchange, symbol), ttl=5)
        data = await ttl_cache.get_or_set(
    key,
    lambda: client.fetch_ticker(exchange, symbol),
    ttl=5
)


        #data = await client.fetch_ticker(exchange, symbol)

        return data
    except ExchangeError as e:
        logger.error("Exchange error: %s", safe_str(e))
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error in get_ticker")
        raise HTTPException(status_code=500, detail='internal error')

@app.get('/historical/{exchange}/{symbol:path}', response_model=OHLCVResponse)
async def get_historical(exchange: str, symbol: str = Path(...), since: int = None, limit: int = 100):
    """
    Return OHLCV data. `since` is milliseconds timestamp or omitted. `limit` default 100.
    """
    try:
        key = f"ohlcv:{exchange}:{symbol}:{since}:{limit}"
        data = await ttl_cache.get_or_set(key, lambda: client.fetch_ohlcv(exchange, symbol, since, limit), ttl=60)
        return {'exchange': exchange, 'symbol': symbol, 'ohlcv': data}
    except ExchangeError as e:
        logger.error("Exchange error: %s", safe_str(e))
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error in get_historical")
        raise HTTPException(status_code=500, detail='internal error')


async def sse_generator(exchange: str, symbol: str, interval: float = 2.0):
    """
    Simple SSE generator (polling-based). Yields lines in SSE format.
    """
    while True:
        try:
            data = await client.fetch_ticker(exchange, symbol)
            # ensure JSON-serializable via built-in conversion (FastAPI will serialize dicts)
            yield f"data: {data}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {{\"error\": \"{safe_str(e)}\"}}\n\n"
        await asyncio.sleep(interval)


@app.get('/sse/ticker/{exchange}/{symbol:path}')
async def sse_ticker(exchange: str, symbol: str, interval: float = 2.0):
    """
    SSE endpoint for near real-time updates. Connect & receive `data: {...}` events.
    """
    return StreamingResponse(sse_generator(exchange, symbol, interval), media_type='text/event-stream')
