# app/api/routes/historical.py

from fastapi import APIRouter, HTTPException
from app.services.exchange_service import ExchangeService
from app.services.cache_service import ohlcv_cache, CacheService

router = APIRouter()

@router.get("/ohlcv")
def get_ohlcv(symbol: str, timeframe: str = "1h", limit: int = 100, exchange: str = "binance"):
    key = f"{exchange}:{symbol}:ohlcv:{timeframe}:{limit}"

    cached = CacheService.get(ohlcv_cache, key)
    if cached:
        return {"source": "cache", "data": cached}

    try:
        service = ExchangeService(exchange)
        data = service.get_ohlcv(symbol, timeframe, limit)
        CacheService.set(ohlcv_cache, key, data)
        return {"source": "api", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))