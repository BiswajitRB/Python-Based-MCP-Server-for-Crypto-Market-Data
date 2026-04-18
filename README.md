# 🚀 MCP Crypto Server

### Real-Time Cryptocurrency Data Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)
![WebSocket](https://img.shields.io/badge/WebSocket-RealTime-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

The **MCP Crypto Server** is a production-ready backend system built using **FastAPI** that provides:

* 📊 Real-time cryptocurrency market data
* 📈 Historical OHLCV data
* ⚡ WebSocket-based live updates
* 🧠 Intelligent caching (in-memory / Redis-ready)
* 🌐 Interactive HTML dashboard

Designed with **scalable architecture**, this project is suitable for both **local development** and **production deployment**.

---

## 🏗️ Architecture

```id="arch001"
Client (Browser / API)
        ↓
 FastAPI Server (MCP)
        ↓
 Service Layer (CCXT)
        ↓
 Crypto Exchanges (Binance, etc.)
        ↓
 Cache Layer (In-Memory / Redis)
```

---

## ⚙️ Tech Stack

| Layer       | Technology              |
| ----------- | ----------------------- |
| Backend     | FastAPI                 |
| Data Source | CCXT                    |
| Realtime    | WebSockets              |
| Caching     | In-Memory (Redis-ready) |
| Frontend    | HTML + JavaScript       |
| Testing     | Pytest                  |
| Deployment  | Docker (optional)       |

---

## 📁 Project Structure

```id="struct001"
mcp-crypto-server/
│
├── app/
│   ├── main.py
│   ├── core/
│   ├── api/routes/
│   ├── services/
│   ├── websocket/
│   ├── cache/
│
├── templates/
│   └── index.html
│
├── static/
│   └── app.js
│
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## 🐍 Virtual Environment Setup

### 🔹 Create Virtual Environment

```bash id="venv1"
python -m venv venv
```

---

### 🔹 Activate Virtual Environment

#### ▶️ Windows (CMD)

```bash id="venv2"
venv\Scripts\activate
```

#### ▶️ Windows (PowerShell)

```bash id="venv3"
venv\Scripts\Activate.ps1
```

#### ▶️ Linux / macOS

```bash id="venv4"
source venv/bin/activate
```

---

### 🔹 Deactivate

```bash id="venv5"
deactivate
```

---

## 🔧 Setup & Installation

### 1️⃣ Clone Repository

```bash id="setup1"
git clone <your-repo-url>
cd mcp-crypto-server
```

---

### 2️⃣ Install Dependencies

```bash id="setup2"
pip install -r requirements.txt
```

---

### 3️⃣ Configure Environment

Create `.env` file:

```env id="setup3"
SYMBOL=BTC/USDT
```

---

### 4️⃣ Run the Server

```bash id="setup4"
python -m uvicorn app.main:app --reload
```

---

## 🌐 Usage

### 🔹 Dashboard

```
http://127.0.0.1:8000
```

### 🔹 API Docs

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### ▶️ Get Market Data

```
GET /market/ticker?symbol=BTC/USDT
```

### ▶️ WebSocket

```
ws://localhost:8000/ws
```

---

## 🧪 Running Tests

```bash id="test1"
pytest
```

---

## 🐳 Docker (Optional)

```bash id="docker1"
docker-compose up --build
```

---

## 🚀 Features

* ✅ Real-time crypto streaming
* ✅ REST API endpoints
* ✅ WebSocket multi-client support
* ✅ Modular clean architecture
* ✅ Error handling & logging
* ✅ Docker-ready
* ✅ Environment configuration

---

## ⚠️ Notes

* Redis is optional (in-memory cache used locally)
* Internet required for live data
* Easily extendable for multi-exchange support

---

## 🚀 Future Improvements

* 📊 Charts (Chart.js / TradingView)
* 🔐 Authentication (JWT)
* 🌍 Multi-coin dashboard
* ☸️ Kubernetes deployment
* 📈 Monitoring (Grafana)

---

## 💼 Resume Highlight

> Built a production-ready crypto market data server using FastAPI, WebSockets, and CCXT with real-time streaming, caching, and scalable architecture.

---

## 👨‍💻 Author

**Biswajit Andia**
MCA Student | Backend & DevOps Enthusiast

---

## 📜 License

MIT License

<img width="1914" height="988" alt="image" src="https://github.com/user-attachments/assets/f5b0af8c-1cb8-473b-8e1c-e6a0c5baab37" />

