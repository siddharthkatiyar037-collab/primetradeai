# 🤖 Binance Testnet Trading Bot

A clean, production-style Python CLI for placing orders on **Binance Spot Testnet**. Supports Market, Limit, and Stop-Market order types with structured logging, input validation, and full error handling.

> **Note:** The Binance Futures Testnet now requires KYC verification. This bot uses the Binance **Spot Testnet** (`https://testnet.binance.vision`) which is functionally identical for demonstrating order placement via REST API — no real funds involved.

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py           # Binance REST client (HMAC signing, requests, error mapping)
│   ├── orders.py           # Order placement logic and response formatting
│   ├── validators.py       # Input validation (symbol, side, type, quantity, price)
│   └── logging_config.py   # Rotating file + console logging setup
├── cli.py                  # CLI entry point (argparse)
├── logs/
│   └── trading_bot.log     # Auto-created on first run
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/trading_bot.git
cd trading_bot
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Binance Testnet API credentials

1. Go to [https://testnet.binance.vision](https://testnet.binance.vision)
2. Click **"Log In with GitHub"** — no KYC required
3. Click **"Generate HMAC_SHA256 Key"**
4. Copy your **API Key** and **Secret Key** — the secret is shown only once

### 5. Set environment variables

**Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY="your_api_key_here"
$env:BINANCE_API_SECRET="your_secret_key_here"
```

**Windows (CMD):**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_secret_key_here
```

**macOS / Linux:**
```bash
export BINANCE_API_KEY=your_api_key_here
export BINANCE_API_SECRET=your_secret_key_here
```

> ⚠️ Never hardcode your API keys in source files. Always use environment variables.

---

## 🚀 How to Run

### Place a Market BUY order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a Limit SELL order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 120000
```

### Place a Stop-Market BUY order *(Bonus feature)*
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.01 --stop-price 95000
```

### View all options
```bash
python cli.py --help
```

---

## 🖥️ Sample Output

**Market BUY:**
```
──────────────────────────────────────────────────
  📋  ORDER REQUEST SUMMARY
──────────────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
──────────────────────────────────────────────────

INFO     Placing BUY MARKET order | symbol=BTCUSDT | qty=0.01

──────────────────────────────────────────────────
  ✅  ORDER PLACED SUCCESSFULLY
──────────────────────────────────────────────────
  Order ID      : 5099704
  Symbol        : BTCUSDT
  Side          : BUY
  Type          : MARKET
  Status        : FILLED
  Quantity      : 0.01000000
  Executed Qty  : 0.01000000
  Avg Price     : N/A
  Time In Force : GTC
──────────────────────────────────────────────────
```

**Limit SELL:**
```
──────────────────────────────────────────────────
  ✅  ORDER PLACED SUCCESSFULLY
──────────────────────────────────────────────────
  Order ID      : 5099809
  Symbol        : BTCUSDT
  Side          : SELL
  Type          : LIMIT
  Status        : NEW
  Quantity      : 0.01000000
  Executed Qty  : 0.00000000
  Avg Price     : N/A
  Limit Price   : 120000.00000000
  Time In Force : GTC
──────────────────────────────────────────────────
```

> `Status: NEW` for a limit order is correct — it means the order is live in the order book, waiting for the price to reach the specified level.

---

## 📋 CLI Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--symbol` | ✅ Yes | Trading pair e.g. `BTCUSDT`, `ETHUSDT` |
| `--side` | ✅ Yes | `BUY` or `SELL` |
| `--type` | ✅ Yes | `MARKET`, `LIMIT`, or `STOP_MARKET` |
| `--quantity` | ✅ Yes | Amount to trade e.g. `0.01` |
| `--price` | ⚠️ LIMIT only | Limit price e.g. `120000` |
| `--stop-price` | ⚠️ STOP_MARKET only | Stop trigger price e.g. `95000` |

---

## 📝 Logging

Logs are written to `logs/trading_bot.log` with automatic rotation (max 5MB, 3 backups kept).

Each entry captures:
- Full API request parameters (with signature)
- Full API response body
- Order placement results
- Validation errors and exceptions

**Log format:**
```
2025-05-18 10:12:01 | DEBUG    | trading_bot.client | REQUEST  POST https://testnet.binance.vision/api/v3/order | params: {...}
2025-05-18 10:12:02 | DEBUG    | trading_bot.client | RESPONSE POST ... | status: 200 | body: {...}
2025-05-18 10:12:02 | INFO     | trading_bot.orders | Order placed successfully | orderId=5099704 | status=FILLED | executedQty=0.01
```

---

## 🛡️ Error Handling

The bot handles the following gracefully with clear error messages:

| Error Type | Example |
|------------|---------|
| Invalid input | Wrong side, missing price for LIMIT |
| Binance API errors | Invalid key, bad symbol, insufficient balance |
| Network failures | No internet, DNS failure |
| Timeouts | Slow or unresponsive API |

---

## 📦 Dependencies

```
requests>=2.31.0
```

Only one external dependency — everything else uses Python's standard library (`hmac`, `hashlib`, `argparse`, `logging`, `urllib`).

---

## 💡 Assumptions

- Uses **Binance Spot Testnet** (`https://testnet.binance.vision`) since Futures Testnet now requires KYC
- Credentials are supplied via environment variables — never hardcoded
- `LIMIT` orders use `timeInForce=GTC` (Good Till Cancelled) by default
- Quantities and prices are passed as-is; Binance enforces symbol-specific precision rules
- The bot places orders only — it does not manage open positions, leverage, or margin

---

## ✨ Bonus Feature

**Stop-Market orders** are supported via `--type STOP_MARKET --stop-price <value>`.  
This places a conditional market order that triggers automatically when the asset price hits the specified stop price — useful for stop-loss and breakout strategies.