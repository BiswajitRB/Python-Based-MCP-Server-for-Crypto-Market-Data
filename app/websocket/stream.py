# app/websocket/stream.py

from fastapi import WebSocket
import asyncio
from app.services.exchange_service import ExchangeService

async def stream_prices(websocket: WebSocket, symbol: str, exchange: str):
    await websocket.accept()
    service = ExchangeService(exchange)

    while True:
        data = service.get_ticker(symbol)
        await websocket.send_json(data)
        await asyncio.sleep(2)