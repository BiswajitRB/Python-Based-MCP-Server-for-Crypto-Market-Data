import json
import asyncio
from fastapi import FastAPI, HTTPException, Request, Path
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

from .exchange_client import ExchangeClient, ExchangeError
from .cache import ttl_cache
from .schemas import TickerResponse, OHLCVResponse
from .utils import logger, safe_str

# FastAPI App
app = FastAPI(
    title="MCP - Market Connector Proxy",
    version="1.0.0"
)

# Templates folder
templates = Jinja2Templates(directory="app/templates")

# Exchange Client
client = ExchangeClient()



# Health Check
@app.get("/health")
async def health():
    return {"status": "ok"}



# Fetch Ticker
@app.get("/ticker/{exchange}/{symbol:path}", response_model=TickerResponse)
async def get_ticker(exchange: str, symbol: str):
    try:
        key = f"ticker:{exchange}:{symbol}"
        data = await ttl_cache.get_or_set(
            key,
            lambda: client.fetch_ticker(exchange, symbol),
            ttl=5
        )
        return data

    except ExchangeError as e:
        logger.error("Exchange error: %s", safe_str(e))
        raise HTTPException(status_code=502, detail=str(e))

    except Exception:
        logger.exception("Unexpected error in /ticker")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# OHLCV Historical Data
@app.get("/historical/{exchange}/{symbol:path}", response_model=OHLCVResponse)
async def get_historical(exchange: str, symbol: str, since: int = None, limit: int = 100):
    try:
        key = f"ohlcv:{exchange}:{symbol}:{since}:{limit}"

        data = await ttl_cache.get_or_set(
            key,
            lambda: client.fetch_ohlcv(exchange, symbol, since, limit),
            ttl=60
        )

        return {
            "exchange": exchange,
            "symbol": symbol,
            "ohlcv": data
        }

    except ExchangeError as e:
        logger.error("Exchange error: %s", safe_str(e))
        raise HTTPException(status_code=502, detail=str(e))

    except Exception:
        logger.exception("Unexpected error in /historical")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# SSE Generator (Real-Time Ticker)
async def sse_generator(exchange: str, symbol: str, interval: float = 2.0):
    while True:
        try:
            data = await client.fetch_ticker(exchange, symbol)
            json_data = json.dumps(data)      # FIX: valid JSON
            yield f"data: {json_data}\n\n"

        except Exception as e:
            error_json = json.dumps({"error": safe_str(e)})
            yield f"event: error\ndata: {error_json}\n\n"

        await asyncio.sleep(interval)

# SSE Endpoint
@app.get("/sse/ticker/{exchange}/{symbol:path}")
async def sse_ticker(exchange: str, symbol: str, interval: float = 2.0):
    return StreamingResponse(
        sse_generator(exchange, symbol, interval),
        media_type="text/event-stream"
    )

# Dashboard HTML Page
@app.get("/dashboard/{exchange}/{symbol:path}")
async def dashboard(request: Request, exchange: str, symbol: str):
    try:
        data = await client.fetch_ticker(exchange, symbol)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "exchange": exchange,
                "symbol": symbol,
                "ticker": data
            }
        )

    except Exception as e:
        logger.exception("Error loading dashboard")
        raise HTTPException(status_code=500, detail=safe_str(e))
