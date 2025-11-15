from pydantic import BaseModel
from typing import Any, List, Optional

class TickerResponse(BaseModel):
    exchange: str
    symbol: str
    timestamp: Optional[int] = None
    datetime: Optional[str] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    last: Optional[float] = None
    volume: Optional[float] = None
    raw: Any = None


class OHLCVResponse(BaseModel):
    exchange: str
    symbol: str
    ohlcv: List[List[Any]]

