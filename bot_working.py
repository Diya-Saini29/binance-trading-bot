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
        
        if not api_key or not api_secret:
            raise Exception("API keys not found in .env file")
        
        # Initialize for demo trading - NO sandbox mode!
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'options': {
                'defaultType': 'future',  # Use futures market
            },
            'urls': {
                'api': {
                    'public': 'https://demo-fapi.binance.com/fapi/v1',
                    'private': 'https://demo-fapi.binance.com/fapi/v1',
                }
            },
            'timeout': 30000,
            'enableRateLimit': True,
        })
        
        # DO NOT call set_sandbox_mode() - that's for the old testnet!
        # You're already using demo endpoints with demo keys
        
        # Test connection
        try:
            logger.info("Connecting to Binance Futures Demo...")
            # Load markets first
            self.exchange.load_markets()
            logger.info(f"✅ Loaded {len(self.exchange.markets)} trading pairs")
            
            # Test with balance fetch
            balance = self.exchange.fetch_balance()
            logger.info("✅ Successfully connected to Binance Futures Demo!")
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def get_balance(self):
        """Get USDT balance in futures account"""
        try:
            balance = self.exchange.fetch_balance()
            # For futures demo, the balance structure might be different
            if 'USDT' in balance:
                return balance['USDT'].get('total', 0)
            elif 'total' in balance:
                return balance['total'].get('USDT', 0)
            else:
                # Try to find any USDT balance
                for currency, data in balance.items():
                    if currency == 'USDT':
                        return data.get('total', 0)
                return 0
        except Exception as e:
            logger.error(f"Failed to fetch balance: {e}")
            return None
    
    def place_market_order(self, symbol, side, quantity):
        """Place a market order"""
        try:
            logger.info(f"Placing {side} MARKET order for {quantity} {symbol}")
            
            if side.upper() == 'BUY':
                order = self.exchange.create_market_buy_order(symbol, quantity)
            else:
                order = self.exchange.create_market_sell_order(symbol, quantity)
            
            logger.info(f"Order successful: {order['id']}")
            return order
        except Exception as e:
            logger.error(f"Order failed: {e}")
            return None
    
    def place_limit_order(self, symbol, side, quantity, price):
        """Place a limit order"""
        try:
            logger.info(f"Placing {side} LIMIT order for {quantity} {symbol} @ {price}")
            
            if side.upper() == 'BUY':
                order = self.exchange.create_limit_buy_order(symbol, quantity, price)
            else:
                order = self.exchange.create_limit_sell_order(symbol, quantity, price)
            
            logger.info(f"Limit order placed: {order['id']}")
            return order
        except Exception as e:
            logger.error(f"Limit order failed: {e}")
            return None

if __name__ == "__main__":
    import sys
    
    try:
        bot = BinanceDemoBot()
        
        if len(sys.argv) > 1 and sys.argv[1] == '--balance':
            balance = bot.get_balance()
            if balance is not None:
                print(f"\n💰 Your Futures Demo Balance: {balance} USDT\n")
            else:
                print("\n❌ Could not fetch balance.\n")
                
        elif len(sys.argv) > 1 and sys.argv[1] == '--order':
            # Usage: python bot_correct.py --order BUY MARKET BTCUSDT 0.001
            try:
                side = sys.argv[2]
                order_type = sys.argv[3]
                symbol = sys.argv[4]
                quantity = float(sys.argv[5])
                
                if order_type.upper() == 'MARKET':
                    result = bot.place_market_order(symbol, side, quantity)
                    if result:
                        print(f"\n✅ {side} MARKET order placed!")
                        print(f"   Order ID: {result['id']}")
                        print(f"   Status: {result['status']}")
                        print(f"   Filled: {result['filled']} / {result['amount']}\n")
                        
                elif order_type.upper() == 'LIMIT':
                    price = float(sys.argv[6])
                    result = bot.place_limit_order(symbol, side, quantity, price)
                    if result:
                        print(f"\n✅ {side} LIMIT order placed at {price}!")
                        print(f"   Order ID: {result['id']}")
                        print(f"   Status: {result['status']}\n")
                        
            except IndexError:
                print("\n❌ Missing arguments!")
                print("Usage examples:")
                print("  MARKET: python bot_correct.py --order BUY MARKET BTCUSDT 0.001")
                print("  LIMIT:  python bot_correct.py --order SELL LIMIT BTCUSDT 0.001 50000\n")
            except Exception as e:
                print(f"\n❌ Order error: {e}\n")
        else:
            print("\n📋 Available commands:")
            print("  python bot_correct.py --balance")
            print("  python bot_correct.py --order BUY MARKET BTCUSDT 0.001")
            print("  python bot_correct.py --order SELL LIMIT BTCUSDT 0.001 50000\n")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you created API keys on demo.binance.com (not testnet)")
        print("2. Verify 'Enable Futures' is checked for your API key")
        print("3. Check your .env file has the correct demo API keys\n")