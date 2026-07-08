import logging

logger = logging.getLogger(__name__)

def validate_symbol(symbol: str) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string (e.g., 'BTCUSDT').")
    
    clean_symbol = symbol.strip().upper()
    
    if len(clean_symbol) < 3 or not clean_symbol.isalnum():
        raise ValueError(f"Invalid symbol format: '{symbol}'. Must be alphanumeric.")
        
    return clean_symbol


def validate_side(side: str) -> str:
    if not side or not isinstance(side, str):
        raise ValueError("Side must be a string: 'BUY' or 'SELL'.")
        
    clean_side = side.strip().upper()
    if clean_side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: '{side}'. Side must be either 'BUY' or 'SELL'.")
        
    return clean_side


def validate_order_type(order_type: str) -> str:
    if not order_type or not isinstance(order_type, str):
        raise ValueError("Order type must be a string: 'MARKET' or 'LIMIT'.")
        
    clean_type = order_type.strip().upper()
    if clean_type not in ['MARKET', 'LIMIT']:
        raise ValueError(f"Invalid order type: '{order_type}'. Supported types are 'MARKET' or 'LIMIT'.")
        
    return clean_type


def validate_quantity(quantity) -> float:
    try:
        qty_float = float(quantity)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid quantity: '{quantity}'. Quantity must be a valid number.")
        
    if qty_float <= 0:
        raise ValueError(f"Invalid quantity: {qty_float}. Quantity must be greater than 0.")
        
    return qty_float


def validate_price(price, order_type: str):
    if order_type == 'MARKET':
        return None
        
    if price is None:
        raise ValueError("Price is required when order type is 'LIMIT'.")
        
    try:
        price_float = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid price: '{price}'. Price must be a valid number.")
        
    if price_float <= 0:
        raise ValueError(f"Invalid price: {price_float}. Price must be greater than 0.")
        
    return price_float


def validate_all_inputs(symbol: str, side: str, order_type: str, quantity, price=None) -> dict:
    logger.info("Executing local input validation...")
    
    try:
        validated_symbol = validate_symbol(symbol)
        validated_side = validate_side(side)
        validated_type = validate_order_type(order_type)
        validated_qty = validate_quantity(quantity)
        validated_price = validate_price(price, validated_type)
        
        logger.info("Local input validation passed successfully.")
        
        return {
            "symbol": validated_symbol,
            "side": validated_side,
            "type": validated_type,
            "quantity": validated_qty,
            "price": validated_price
        }
        
    except ValueError as e:
        logger.warning(f"Local validation failed: {str(e)}")
        raise e