#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot — CLI Entry Point
"""

import argparse
import os
import sys

from bot.client import BinanceAPIError, BinanceClient
from bot.logging_config import setup_logging
from bot.orders import format_order_response, place_order
from bot.validators import ValidationError, validate_order_params

logger = setup_logging().getChild("cli")


def get_credentials() -> tuple[str, str]:
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        print(
            "\n❌  Missing API credentials.\n"
            "    Set environment variables before running:\n"
            "      export BINANCE_API_KEY=your_key\n"
            "      export BINANCE_API_SECRET=your_secret\n"
        )
        sys.exit(1)
    return api_key, api_secret


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  Market BUY:\n"
            "    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01\n\n"
            "  Limit SELL:\n"
            "    python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500\n\n"
            "  Stop-Market BUY (bonus):\n"
            "    python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.01 --stop-price 95000\n"
        ),
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument(
        "--type",
        dest="order_type",
        required=True,
        help="Order type: MARKET | LIMIT | STOP_MARKET",
    )
    parser.add_argument("--quantity", required=True, help="Quantity to trade")
    parser.add_argument("--price", default=None, help="Limit price (required for LIMIT)")
    parser.add_argument(
        "--stop-price", dest="stop_price", default=None, help="Stop price (required for STOP_MARKET)"
    )
    return parser


def print_request_summary(params: dict) -> None:
    print()
    print("─" * 50)
    print("  📋  ORDER REQUEST SUMMARY")
    print("─" * 50)
    print(f"  Symbol     : {params['symbol']}")
    print(f"  Side       : {params['side']}")
    print(f"  Type       : {params['order_type']}")
    print(f"  Quantity   : {params['quantity']}")
    if "price" in params:
        print(f"  Price      : {params['price']}")
    if "stop_price" in params:
        print(f"  Stop Price : {params['stop_price']}")
    print("─" * 50)
    print()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Validate inputs
    try:
        params = validate_order_params(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except ValidationError as e:
        logger.error("Validation failed: %s", e)
        print(f"\n❌  Validation error: {e}\n")
        sys.exit(1)

    print_request_summary(params)

    # Get credentials and create client
    api_key, api_secret = get_credentials()
    client = BinanceClient(api_key, api_secret)

    # Place the order
    try:
        response = place_order(
            client=client,
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params.get("price"),
            stop_price=params.get("stop_price"),
        )
        print(format_order_response(response))

    except ValidationError as e:
        logger.error("Validation error: %s", e)
        print(f"\n❌  Validation error: {e}\n")
        sys.exit(1)

    except BinanceAPIError as e:
        logger.error("Binance API error [%s]: %s", e.code, e.message)
        print(f"\n❌  Binance API error (code {e.code}): {e.message}\n")
        sys.exit(1)

    except ConnectionError as e:
        logger.error("Connection error: %s", e)
        print(f"\n❌  Connection error: {e}\n")
        sys.exit(1)

    except TimeoutError as e:
        logger.error("Timeout: %s", e)
        print(f"\n❌  Timeout: {e}\n")
        sys.exit(1)

    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        print(f"\n❌  Unexpected error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
