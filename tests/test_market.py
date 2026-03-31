from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ticker():
    response = client.get("/ticker?symbol=BTC/USDT")
    assert response.status_code == 200
    assert "data" in response.json()