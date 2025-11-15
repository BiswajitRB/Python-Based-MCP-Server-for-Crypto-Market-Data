import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
import asyncio

# We'll monkeypatch the client instance inside app.main to use dummy values
@pytest.fixture(autouse=True)
def patch_exchange(monkeypatch):
    class DummyClient:
        async def fetch_ticker(self, exchange, symbol):
            return {
                'exchange': exchange,
                'symbol': symbol,
                'timestamp': 1234567890,
                'datetime': '2025-01-01T00:00:00Z',
                'bid': 100.0,
                'ask': 101.0,
                'last': 100.5,
                'volume': 12.34,
                'raw': {}
            }
        async def fetch_ohlcv(self, exchange, symbol, since, limit):
            # two sample candles [timestamp, open, high, low, close, volume]
            return [[1234560000, 90, 110, 85, 105, 10], [1234560060, 100, 120, 95, 110, 5]]

    monkeypatch.setattr('app.main.client', DummyClient())

def test_health():
    client = TestClient(app)
    r = client.get('/health')
    assert r.status_code == status.HTTP_200_OK
    assert r.json()['status'] == 'ok'

def test_ticker():
    client = TestClient(app)
    # symbol with slash must be URL-encoded or use path capture. Here we use path capture by placing slash directly.
    r = client.get('/ticker/binance/BTC%2FUSDT')  # URL-encoded slash
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data['exchange'] == 'binance'
    assert data['symbol'] in ('BTC/USDT', 'BTC%2FUSDT', 'BTC')  # flexible check

def test_historical():
    client = TestClient(app)
    r = client.get('/historical/binance/BTC%2FUSDT')
    assert r.status_code == status.HTTP_200_OK
    d = r.json()
    assert 'ohlcv' in d
    assert isinstance(d['ohlcv'], list)

