from typing import Optional

from .client import BinanceClient
from .logging_config import setup_logging

logger = setup_logging().getChild("orders")

ORDER_ENDPOINT = "/api/v3/order"


def _build_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    stop_price: Optional[str] = None,
) -> dict:
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }
    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"
    if order_type == "STOP_MARKET":
        params["stopPrice"] = stop_price
    return params


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    stop_price: Optional[str] = None,
) -> dict:
    params = _build_params(symbol, side, order_type, quantity, price, stop_price)

    logger.info(
        "Placing %s %s order | symbol=%s | qty=%s%s%s",
        side,
        order_type,
        symbol,
        quantity,
        f" | price={price}" if price else "",
        f" | stopPrice={stop_price}" if stop_price else "",
    )

    response = client.post(ORDER_ENDPOINT, params)

    logger.info(
        "Order placed successfully | orderId=%s | status=%s | executedQty=%s | avgPrice=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
        response.get("avgPrice"),
    )

    return response


def format_order_response(response: dict) -> str:
    lines = [
        "",
        "─" * 50,
        "  ✅  ORDER PLACED SUCCESSFULLY",
        "─" * 50,
        f"  Order ID      : {response.get('orderId', 'N/A')}",
        f"  Symbol        : {response.get('symbol', 'N/A')}",
        f"  Side          : {response.get('side', 'N/A')}",
        f"  Type          : {response.get('type', 'N/A')}",
        f"  Status        : {response.get('status', 'N/A')}",
        f"  Quantity      : {response.get('origQty', 'N/A')}",
        f"  Executed Qty  : {response.get('executedQty', 'N/A')}",
        f"  Avg Price     : {response.get('avgPrice', 'N/A')}",
    ]
    if response.get("price") and response["price"] != "0":
        lines.append(f"  Limit Price   : {response.get('price', 'N/A')}")
    if response.get("stopPrice") and response["stopPrice"] != "0":
        lines.append(f"  Stop Price    : {response.get('stopPrice', 'N/A')}")
    lines += [
        f"  Time In Force : {response.get('timeInForce', 'N/A')}",
        f"  Created At    : {response.get('updateTime', 'N/A')}",
        "─" * 50,
        "",
    ]
    return "\n".join(lines)
