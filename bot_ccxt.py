import ccxt
import os
from dotenv import load_dotenv
import logging
import sys

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BinanceTestnetBot:
    def __init__(self):
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            raise Exception("API keys not found! Please check your .env file")
        
        # Initialize Binance Futures with testnet configuration
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'options': {
                'defaultType': 'future',  # Use futures market
            },
            'urls': {
                'api': {
                    'public': 'https://testnet.binancefuture.com/fapi/v1',
                    'private': 'https://testnet.binancefuture.com/fapi/v1',
                }
            }
        })
        
        # Enable testnet mode
        self.exchange.set_sandbox_mode(True)
        
        # Test connection
        try:
            balance = self.exchange.fetch_balance()
            logger.info("✅ Successfully connected to Binance Futures Testnet")
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


# CLI Interface
if __name__ == "__main__":
    
    bot = BinanceTestnetBot()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--balance':
        balance = bot.get_balance()
        print(f"\n💰 Your Testnet Balance: {balance} USDT\n")
    
    elif len(sys.argv) > 1 and sys.argv[1] == '--order':
        # Usage: python bot_ccxt.py --order BUY MARKET BTCUSDT 0.001
        #        python bot_ccxt.py --order SELL LIMIT BTCUSDT 0.001 50000
        try:
            side = sys.argv[2]
            order_type = sys.argv[3]
            symbol = sys.argv[4]
            quantity = float(sys.argv[5])
            
            if order_type.upper() == 'MARKET':
                result = bot.place_market_order(symbol, side, quantity)
                if result:
                    print(f"\n✅ {side} MARKET order placed successfully!")
                    print(f"   Order ID: {result['id']}")
                    print(f"   Status: {result['status']}")
                    print(f"   Symbol: {result['symbol']}")
                    print(f"   Quantity: {result['amount']}\n")
                    
            elif order_type.upper() == 'LIMIT':
                price = float(sys.argv[6])
                result = bot.place_limit_order(symbol, side, quantity, price)
                if result:
                    print(f"\n✅ {side} LIMIT order placed at {price}!")
                    print(f"   Order ID: {result['id']}")
                    print(f"   Status: {result['status']}")
                    print(f"   Symbol: {result['symbol']}")
                    print(f"   Quantity: {result['amount']}\n")
            else:
                print("Order type must be MARKET or LIMIT")
                
        except IndexError:
            print("\n❌ Missing arguments!")
            print("\nUsage examples:")
            print("  MARKET: python bot_ccxt.py --order BUY MARKET BTCUSDT 0.001")
            print("  LIMIT:  python bot_ccxt.py --order SELL LIMIT BTCUSDT 0.001 50000")
            print("  BALANCE: python bot_ccxt.py --balance\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
    else:
        print("\n❌ Unknown command!")
        print("\nAvailable commands:")
        print("  python bot_ccxt.py --balance")
        print("  python bot_ccxt.py --order BUY MARKET BTCUSDT 0.001")
        print("  python bot_ccxt.py --order SELL LIMIT BTCUSDT 0.001 50000\n")