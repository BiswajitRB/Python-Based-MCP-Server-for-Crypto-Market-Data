# app/api/routes/market.py

from fastapi import APIRouter, HTTPException
from app.services.exchange_service import ExchangeService
from app.services.cache_service import ticker_cache, CacheService

router = APIRouter()

@router.get("/ticker")
def get_ticker(symbol: str, exchange: str = "binance"):
    key = f"{exchange}:{symbol}:ticker"

    cached = CacheService.get(ticker_cache, key)
    if cached:
        return {"source": "cache", "data": cached}

    try:
        service = ExchangeService(exchange)
        data = service.get_ticker(symbol)
        CacheService.set(ticker_cache, key, data)
        return {"source": "api", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))