#!/usr/bin/env python3
import argparse
import sys
import os
from dotenv import load_dotenv

from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient
from bot.validators import *
from bot.orders import OrderManager

load_dotenv()
logger = setup_logging()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Binance Futures Testnet Trading Bot',
        epilog="""
Examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 50000
  python cli.py --balance
        """
    )
    
    parser.add_argument('--symbol', '-s', type=str, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', '-sd', type=str, choices=['BUY', 'SELL'], help='BUY or SELL')
    parser.add_argument('--type', '-t', type=str, choices=['MARKET', 'LIMIT'], help='MARKET or LIMIT')
    parser.add_argument('--quantity', '-q', type=float, help='How much to trade')
    parser.add_argument('--price', '-p', type=float, help='Price for LIMIT orders')
    parser.add_argument('--balance', '-b', action='store_true', help='Show account balance')
    parser.add_argument('--api-key', type=str, help='Binance API key')
    parser.add_argument('--api-secret', type=str, help='Binance API secret')
    
    return parser.parse_args()

def get_api_credentials(args):
    api_key = args.api_key or os.getenv('BINANCE_API_KEY')
    api_secret = args.api_secret or os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        logger.error("❌ API keys not found!")
        logger.error("Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file")
        sys.exit(1)
    
    return api_key, api_secret

def main():
    args = parse_arguments()
    
    if args.balance:
        api_key, api_secret = get_api_credentials(args)
        client = BinanceFuturesClient(api_key, api_secret)
        balance = client.get_account_balance()
        print(f"\n💰 Your Testnet Balance: {balance} USDT\n")
        return
    
    if not all([args.symbol, args.side, args.type, args.quantity]):
        logger.error("❌ Missing required arguments!")
        logger.error("You need: --symbol, --side, --type, --quantity")
        logger.error("Use --help for examples")
        sys.exit(1)
    
    if not validate_symbol(args.symbol):
        sys.exit(1)
    if not validate_side(args.side):
        sys.exit(1)
    if not validate_order_type(args.type):
        sys.exit(1)
    
    valid, msg = validate_quantity(args.quantity)
    if not valid:
        logger.error(f"❌ {msg}")
        sys.exit(1)
    
    if args.type == 'LIMIT':
        valid, msg = validate_price(args.price)
        if not valid:
            logger.error(f"❌ {msg}")
            sys.exit(1)
    
    api_key, api_secret = get_api_credentials(args)
    
    try:
        logger.info("Connecting to Binance Futures Testnet...")
        client = BinanceFuturesClient(api_key, api_secret)
        order_manager = OrderManager(client)
        
        result = order_manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
        
        print(order_manager.format_order_output(result))
        sys.exit(0 if result['success'] else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()