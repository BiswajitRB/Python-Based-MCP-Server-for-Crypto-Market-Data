# app/main.py

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from app.api.routes import market, historical, health
from app.websocket.stream import stream_prices

app = FastAPI(title="MCP Crypto Server")

# Include API routes
app.include_router(market.router)
app.include_router(historical.router)
app.include_router(health.router)

# Root (optional but recommended)
@app.get("/")
def root():
    return {"message": "MCP Crypto Server Running 🚀"}

# Serve Graph UI
@app.get("/graph")
def get_graph():
    return FileResponse("app/static/index.html")

# WebSocket for real-time data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, symbol: str = "BTC/USDT", exchange: str = "binance"):
    await stream_prices(websocket, symbol, exchange)