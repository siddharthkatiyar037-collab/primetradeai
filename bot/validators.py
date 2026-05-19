from decimal import Decimal, InvalidOperation


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s or not s.isalpha():
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Must be alphabetic (e.g. BTCUSDT)."
        )
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side '{side}'. Must be one of: {', '.join(sorted(VALID_SIDES))}."
        )
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )
    return t


def validate_quantity(quantity: str) -> str:
    try:
        q = Decimal(str(quantity))
        if q <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return str(q)
    except InvalidOperation:
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a positive number.")


def validate_price(price: str) -> str:
    try:
        p = Decimal(str(price))
        if p <= 0:
            raise ValidationError("Price must be greater than zero.")
        return str(p)
    except InvalidOperation:
        raise ValidationError(f"Invalid price '{price}'. Must be a positive number.")


def validate_stop_price(stop_price: str) -> str:
    return validate_price(stop_price)


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str = None,
    stop_price: str = None,
) -> dict:
    """Validate all order parameters and return a cleaned dict."""
    params = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
    }

    if params["order_type"] == "LIMIT":
        if not price:
            raise ValidationError("Price is required for LIMIT orders.")
        params["price"] = validate_price(price)

    if params["order_type"] == "STOP_MARKET":
        if not stop_price:
            raise ValidationError("Stop price is required for STOP_MARKET orders.")
        params["stop_price"] = validate_stop_price(stop_price)

    return params
