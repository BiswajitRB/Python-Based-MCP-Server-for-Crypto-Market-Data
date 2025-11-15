# MCP (Market Connector Proxy) - Python Crypto Data Server

## Overview
This repository implements a Python-based MCP server to retrieve real-time and historical cryptocurrency market data from major exchanges using `ccxt`. It includes:
- FastAPI server with REST endpoints and an SSE endpoint for lightweight real-time updates.
- Exchange client wrapper (`ccxt`-based) that standardizes ticker and historical OHLCV retrieval.
- In-memory caching with TTL to reduce API calls and improve performance.
- Structured error handling and utilities.
- Thorough test cases using `pytest` and `pytest-asyncio` with function-level mocking to avoid live API calls during tests.

## Features / Endpoints
- `GET /health` - simple health check.
- `GET /ticker/{exchange}/{symbol}` - current market ticker (bid/ask/last/volume) fetched from exchange.
- `GET /historical/{exchange}/{symbol}` - historical OHLCV (since & limit query params supported).
- `GET /sse/ticker/{exchange}/{symbol}` - Server-Sent Events stream for near-real-time updates (polling-based).

## Notes & Assumptions
- Uses `ccxt` for interacting with exchanges (public endpoints). No API keys are required for public market data. You may add keys to `ExchangeClient` if needed for private endpoints.
- This scaffold focuses on correctness, structure, tests, and extensibility. In production, replace in-memory cache with Redis or similar, add rate-limiting, robust auth, and monitoring.
- The test suite **mocks** the exchange client to avoid network calls; therefore tests run offline.

## Setup (local)
1. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .\.venv\Scripts\activate # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server (development):
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Run tests:
   ```bash
   pytest -q
   ```

## Files
- `app/` - FastAPI app and implementation.
- `tests/` - test cases using pytest.
- `requirements.txt` - suggested Python dependencies.

## Deployment & GitHub
- This package is ready to be pushed to GitHub. After pushing, provide the repo URL as requested.

