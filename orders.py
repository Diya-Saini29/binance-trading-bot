
import logging
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger(__name__)

class OrderManager:
    
    def __init__(self, client):
        self.client = client
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                    quantity: float, price: float = None):
        
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()
        
        logger.info(f"Order request: {order_type} {side} {quantity} {symbol}")
        if price:
            logger.info(f"Limit price: {price}")
        
        try:
            if order_type == 'MARKET':
                order = self.client.place_market_order(symbol, side, quantity)
            elif order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders")
                order = self.client.place_limit_order(symbol, side, quantity, price)
            else:
                raise ValueError(f"Unknown order type: {order_type}")
            
            return {
                'success': True,
                'order_id': order.get('orderId'),
                'symbol': order.get('symbol'),
                'side': order.get('side'),
                'type': order.get('type'),
                'quantity': order.get('origQty'),
                'price': order.get('price'),
                'executed_qty': order.get('executedQty'),
                'avg_price': order.get('avgPrice'),
                'status': order.get('status')
            }
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message}")
            return {
                'success': False,
                'error_message': f"Binance Error: {e.message}"
            }
        except BinanceRequestException as e:
            logger.error(f"Network Error: {str(e)}")
            return {
                'success': False,
                'error_message': f"Network Error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'success': False,
                'error_message': f"Error: {str(e)}"
            }
    
    def format_order_output(self, result: dict) -> str:
        if result['success']:
            return f"""
{'='*50}
✅ ORDER SUCCESSFUL
{'='*50}
Order ID:     {result['order_id']}
Symbol:       {result['symbol']}
Side:         {result['side']}
Type:         {result['type']}
Quantity:     {result['quantity']}
Status:       {result['status']}
Executed Qty: {result['executed_qty']}
Avg Price:    {result['avg_price']}
{'='*50}
"""
        else:
            return f"""
{'='*50}
❌ ORDER FAILED
{'='*50}
Error: {result['error_message']}
{'='*50}
"""