# Simplified Binance Futures Trading Bot

A structured Python command-line application designed to execute and manage orders on the Binance Futures Testnet (USDT-M) safely using `uv`. This application includes input validation, robust exception handling, and explicit execution logging.

## Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── client.py            # Authenticates and configures the Binance Testnet Client
│   ├── logging_config.py    # Global logger implementation (Rotating file handler)
│   ├── orders.py            # Trade execution engine (MARKET, LIMIT, STOP)
│   └── validators.py        # User input validation
├── logs/
│   └── trading_bot.log      # Auto-generated runtime logs (Git ignored)
├── .env                     # Private environment API credentials (Git ignored)
├── .gitignore               # Ensures secure, clean repository commits
├── main.py                  # CLI application orchestration entry point
└── pyproject.toml           # Project metadata and dependencies managed by uv
```

## Prerequisites and Installation

Project uses UV for fast, reproducible dependency and environment management.
1. Ensure uv is installed on your local machine.

2. Clone this repository and navigate to the project root directory.

3. Install the required dependencies securely within the project workspace:

```text
  uv sync
```

The application authenticates requests using a secure local environment file. Create a file named .env in the root directory and add your Binance Futures Testnet API credentials:
```text
  API_KEY=your_binance_testnet_api_key_here
  API_SECRET=your_binance_testnet_secret_key_here
```

## Examples
### 1. Execute a Market Order (BUY)
Places an immediate trade at the current market price. The execution engine automatically sleeps for 1.5 seconds post-submission to poll the exchange for the final filled quantity and execution price.
```text
  uv run main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 2. Execute a Limit Order (SELL)
Places a resting order on the exchange book that will only execute if the asset hits your exact target price.
```text
  uv run main.py -s BTCUSDT -d SELL -t LIMIT -q 0.01 -p 65000
```

### 3. Execute a Stop-Limit Order (STOP)
Places a conditional algorithmic order that remains on the Algo Server until the trigger (--stop-price) is struck, which then releases a limit order at your targeted execution price.
```text
  uv run main.py -s BTCUSDT -d SELL -t STOP -q 0.01 -p 60000 -sp 61000
```

## Example Log Outputs

All internal runtime operations, input validation phases, and remote exchange API communication states are quietly recorded within `logs/trading_bot.log`. The configuration utilizes a rolling handler that formats entries uniformly: 
`[TIMESTAMP] LEVEL [MODULE:LINE] MESSAGE`

### 1. Successful Market Order Pipeline (With Polling)
```text
[2026-07-08 19:37:59] INFO [cli_entry:13] Trading bot CLI tool executed.
[2026-07-08 19:37:59] INFO [bot.validators:84] Executing local input validation...
[2026-07-08 19:37:59] INFO [bot.validators:94] Local input validation passed successfully.
[2026-07-08 19:37:59] INFO [bot.client:14] Making connection to Binance ....
[2026-07-08 19:37:59] INFO [bot.client:19] Connected to the Binance Future Testnet.
[2026-07-08 19:37:59] INFO [bot.orders:43] Sending order payload to Binance Futures API: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01}
[2026-07-08 19:38:00] INFO [bot.orders:48] Order successfully placed. Raw API Response: {'orderId': 20124500736, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJa3eb6375d129435aec7bfe', 'price': '0.00', 'origQty': '0.0100', 'executedQty': '0.0000', 'cumQty': '0.0000', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1783519680097}
[2026-07-08 19:38:02] INFO [bot.orders:57] Order updated. New Response: {'orderId': 20124500736, 'symbol': 'BTCUSDT', 'status': 'FILLED', 'clientOrderId': 'x-Cb7ytekJa3eb6375d129435aec7bfe', 'price': '0.00', 'avgPrice': '61981.200000', 'origQty': '0.0100', 'executedQty': '0.0100', 'cumQuote': '619.812000', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'time': 1783519680097, 'updateTime': 1783519680097}
```

### 2. Successful Limit Order Pipeline
```text
[2026-07-08 19:38:25] INFO [cli_entry:13] Trading bot CLI tool executed.
[2026-07-08 19:38:25] INFO [bot.validators:84] Executing local input validation...
[2026-07-08 19:38:25] INFO [bot.validators:94] Local input validation passed successfully.
[2026-07-08 19:38:25] INFO [bot.client:14] Making connection to Binance ....
[2026-07-08 19:38:26] INFO [bot.client:19] Connected to the Binance Future Testnet.
[2026-07-08 19:38:26] INFO [bot.orders:43] Sending order payload to Binance Futures API: {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'LIMIT', 'quantity': 0.01, 'price': 65000.0, 'timeInForce': 'GTC'}
[2026-07-08 19:38:26] INFO [bot.orders:48] Order successfully placed. Raw API Response: {'orderId': 20124590732, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-Cb7ytekJd732e915373ad3af71ab15', 'price': '65000.00', 'origQty': '0.0100', 'executedQty': '0.0000', 'cumQty': '0.0000', 'timeInForce': 'GTC', 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'EXPIRE_MAKER', 'goodTillDate': 0, 'updateTime': 1783519706295}
```