import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance.enums import *

logger = logging.getLogger(__name__)

TESTNET_BASE_URL = "https://testnet.binancefuture.com"

class BinanceFuturesClient:
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        
        try:
            self.client = Client(api_key, api_secret, testnet=True)
            self.client.futures_base_url = TESTNET_BASE_URL
            self.client.futures_account()
            logger.info("Successfully connected to Binance Futures Testnet")
            
        except BinanceAPIException as e:
            logger.error(f"API Error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float):
        try:
            logger.info(f"Placing MARKET {side} order for {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            
            logger.info(f"Order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"API Error: {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Network Error: {str(e)}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        try:
            logger.info(f"Placing LIMIT {side} order for {quantity} {symbol} @ {price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=str(price),
                timeInForce='GTC'
            )
            
            logger.info(f"Order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"API Error: {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Network Error: {str(e)}")
            raise
    
    def get_account_balance(self):
        try:
            account = self.client.futures_account()
            return account.get('totalWalletBalance', 'N/A')
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            return None