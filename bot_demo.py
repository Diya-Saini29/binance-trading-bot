import ccxt
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BinanceDemoBot:
    def __init__(self):
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        # Initialize Binance with demo trading
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'options': {
                'defaultType': 'future',
            }
        })
        
        # Enable demo trading (this is the key change!)
        self.exchange.enable_demo_trading(True)
        
        # Test connection
        try:
            balance = self.exchange.fetch_balance()
            logger.info("✅ Successfully connected to Binance Demo Trading")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def get_balance(self):
        """Get USDT balance"""
        try:
            balance = self.exchange.fetch_balance()
            usdt_balance = balance['total'].get('USDT', 0)
            return usdt_balance
        except Exception as e:
            logger.error(f"Failed to fetch balance: {e}")
            return None
    
    def place_market_order(self, symbol, side, quantity):
        """Place a market order"""
        try:
            if side.upper() == 'BUY':
                order = self.exchange.create_market_buy_order(symbol, quantity)
            else:
                order = self.exchange.create_market_sell_order(symbol, quantity)
            
            logger.info(f"Order placed: {order}")
            return order
        except Exception as e:
            logger.error(f"Order failed: {e}")
            return None
    
    def place_limit_order(self, symbol, side, quantity, price):
        """Place a limit order"""
        try:
            if side.upper() == 'BUY':
                order = self.exchange.create_limit_buy_order(symbol, quantity, price)
            else:
                order = self.exchange.create_limit_sell_order(symbol, quantity, price)
            
            logger.info(f"Limit order placed: {order}")
            return order
        except Exception as e:
            logger.error(f"Limit order failed: {e}")
            return None

if __name__ == "__main__":
    import sys
    
    bot = BinanceDemoBot()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--balance':
        balance = bot.get_balance()
        print(f"\n💰 Your Demo Balance: {balance} USDT\n")
    
    elif len(sys.argv) > 1 and sys.argv[1] == '--order':
        try:
            side = sys.argv[2]
            order_type = sys.argv[3]
            symbol = sys.argv[4]
            quantity = float(sys.argv[5])
            
            if order_type.upper() == 'MARKET':
                result = bot.place_market_order(symbol, side, quantity)
                if result:
                    print(f"\n✅ {side} MARKET order placed!")
                    print(f"   Order ID: {result['id']}\n")
                    
            elif order_type.upper() == 'LIMIT':
                price = float(sys.argv[6])
                result = bot.place_limit_order(symbol, side, quantity, price)
                if result:
                    print(f"\n✅ {side} LIMIT order placed at {price}!\n")
                    
        except Exception as e:
            print(f"\n❌ Error: {e}\n")