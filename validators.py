import logging

logger = logging.getLogger(__name__)

def validate_symbol(symbol: str) -> bool:
    """Check if the trading pair symbol is valid."""
    if not symbol or not isinstance(symbol, str):
        return False
    
    symbol = symbol.upper()
    
    if not symbol.endswith('USDT'):
        logger.warning(f"Symbol '{symbol}' does not end with USDT")
        return False
    
    if len(symbol) < 6:
        logger.warning(f"Symbol '{symbol}' is too short")
        return False
    
    return True

def validate_quantity(quantity: float) -> tuple:
    """Check if quantity is valid."""
    if quantity is None:
        return False, "Quantity is required"
    
    if not isinstance(quantity, (int, float)):
        return False, f"Quantity must be a number"
    
    if quantity <= 0:
        return False, f"Quantity must be positive, got {quantity}"
    
    if quantity < 0.001:
        return False, f"Quantity {quantity} is below minimum 0.001"
    
    return True, None

def validate_price(price: float) -> tuple:
    """Check if limit order price is valid."""
    if price is None:
        return False, "Price is required for LIMIT orders"
    
    if not isinstance(price, (int, float)):
        return False, f"Price must be a number"
    
    if price <= 0:
        return False, f"Price must be positive, got {price}"
    
    return True, None

def validate_side(side: str) -> bool:
    """Check if side is BUY or SELL"""
    if not side:
        return False
    side = side.upper()
    return side in ['BUY', 'SELL']

def validate_order_type(order_type: str) -> bool:
    """Check if order type is MARKET or LIMIT"""
    if not order_type:
        return False
    order_type = order_type.upper()
    return order_type in ['MARKET', 'LIMIT']