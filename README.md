# Binance Futures Testnet Trading Bot

A Python CLI application for placing MARKET and LIMIT orders on Binance Futures Testnet.

## Features

- ✅ Place MARKET orders (BUY/SELL)
- ✅ Place LIMIT orders (BUY/SELL)
- ✅ CLI interface with argument parsing
- ✅ Comprehensive logging (file + console)
- ✅ Input validation for all parameters
- ✅ Error handling for API errors and network failures

## Tech Stack

- Python 3.10+
- python-binance library
- python-dotenv for API key management
- Logging module for audit trails

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/binance-trading-bot.git
cd binance-trading-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
