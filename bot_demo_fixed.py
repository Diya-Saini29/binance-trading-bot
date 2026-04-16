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
        
        # Initialize with longer timeout
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'options': {
                'defaultType': 'future',
            },
            'timeout': 30000,  # 30 seconds timeout (increased from default)
            'enableRateLimit': True,
        })
        
        # Enable demo trading
        self.exchange.enable_demo_trading(True)
        
        # Test connection with retry
        try:
            logger.info("Connecting to Binance Demo Trading...")
            balance = self.exchange.fetch_balance()
            logger.info("✅ Successfully connected!")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise
    
    def get_balance(self):
        try:
            balance = self.exchange.fetch_balance()
            usdt_balance = balance['total'].get('USDT', 0)
            return usdt_balance
        except Exception as e:
            logger.error(f"Failed to fetch balance: {e}")
            return None

if __name__ == "__main__":
    import sys
    
    try:
        bot = BinanceDemoBot()
        
        if len(sys.argv) > 1 and sys.argv[1] == '--balance':
            balance = bot.get_balance()
            if balance is not None:
                print(f"\n💰 Your Demo Balance: {balance} USDT\n")
            else:
                print("\n❌ Could not fetch balance. Check your internet connection.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Temporarily disable firewall/VPN")
        print("3. Try again in a few minutes\n")