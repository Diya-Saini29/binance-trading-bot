from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

print(f"API Key: {api_key[:10]}...")  # Shows first 10 characters
print(f"Secret found: {'Yes' if api_secret else 'No'}")