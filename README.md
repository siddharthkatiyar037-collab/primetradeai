# Binance Futures Testnet Trading Bot

A clean, production-style Python CLI for placing orders on Binance Futures Testnet (USDT-M). Supports Market, Limit, and Stop-Market order types with structured logging and full error handling.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST API client (signing, requests, error mapping)
│   ├── orders.py          # Order placement logic and response formatting
│   ├── validators.py      # Input validation (symbol, side, type, quantity, price)
│   └── logging_config.py  # Rotating file + console logging setup
├── cli.py                 # CLI entry point (argparse)
├── logs/                  # Auto-created; contains trading_bot.log
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/trading_bot.git
cd trading_bot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Get Binance Futures Testnet credentials

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with your GitHub account
3. Navigate to **API Key** section and generate a key pair

### 4. Set environment variables

```bash
export BINANCE_API_KEY=your_api_key_here
export BINANCE_API_SECRET=your_api_secret_here
```

On Windows (cmd):
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

---

## How to Run

### Place a Market BUY order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a Limit SELL order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 120000
```

### Place a Stop-Market BUY order (bonus feature)

```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.01 --stop-price 95000
```

### View full help

```bash
python cli.py --help
```

---

## Sample Output

```
──────────────────────────────────────────────────
  📋  ORDER REQUEST SUMMARY
──────────────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
──────────────────────────────────────────────────

──────────────────────────────────────────────────
  ✅  ORDER PLACED SUCCESSFULLY
──────────────────────────────────────────────────
  Order ID      : 3294042965
  Symbol        : BTCUSDT
  Side          : BUY
  Type          : MARKET
  Status        : FILLED
  Quantity      : 0.01
  Executed Qty  : 0.01
  Avg Price     : 96580.50000
  Time In Force : GTC
  Created At    : 1716000000000
──────────────────────────────────────────────────
```

---

## Logging

Logs are stored in `logs/trading_bot.log` with rotation (max 5MB, 3 backups).

Each log entry captures:
- Full API request parameters
- Full API response body
- Validation errors and exceptions

Log format:
```
2025-01-01 12:00:00 | DEBUG    | trading_bot.client | REQUEST  POST https://testnet.binancefuture.com/fapi/v1/order | params: {...}
2025-01-01 12:00:01 | DEBUG    | trading_bot.client | RESPONSE POST ... | status: 200 | body: {...}
2025-01-01 12:00:01 | INFO     | trading_bot.orders | Order placed successfully | orderId=3294042965 | status=FILLED | ...
```

---

## Assumptions

- Only USDT-M futures are supported (base URL: `https://testnet.binancefuture.com`)
- Credentials are passed via environment variables (not hardcoded)
- LIMIT orders use `timeInForce=GTC` by default
- Quantities and prices are passed as-is; Binance enforces exchange-specific precision rules
- The bot does not manage positions, leverage, or margin — it only places orders

---

## Bonus Feature

**Stop-Market orders** are supported via `--type STOP_MARKET --stop-price <value>`. This allows placing conditional orders that trigger at a specified price level.
