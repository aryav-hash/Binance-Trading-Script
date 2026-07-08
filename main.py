import argparse
import sys
import logging

from bot.logging_config import setup_logging
from bot.client import BinanceTestnetClient
from bot.validators import validate_all_inputs
from bot.orders import place_future_orders

def main():
    setup_logging()
    logger = logging.getLogger("cli_entry")
    logger.info("Trading bot CLI tool executed.")

    parser = argparse.ArgumentParser(
        description="Command Line Interface for placing Binance Futures Testnet orders safely."
    )

    parser.add_argument("--symbol", "-s", required=True, help="The crypto asset pair (e.g., BTCUSDT).")
    parser.add_argument("--side", "-d", required=True, help="The trade execution action: BUY or SELL.")
    parser.add_argument("--type", "-t", required=True, help="Order type: MARKET or LIMIT.")
    parser.add_argument("--quantity", "-q", required=True, help="The volume size of the asset to trade.")
    parser.add_argument("--price", "-p", required=False, default=None, help="Target price (Mandatory for LIMIT).")
    parser.add_argument("--stop-price", "-sp", required=False, default=None, help="The trigger price (Mandatory for STOP).")

    args = parser.parse_args()

    try:
        validated_inputs = validate_all_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )
    except ValueError as e:
        print(f"\n[VALIDATION FAILED] {str(e)}")
        sys.exit(1)
    
    try:
        bot_wrapper = BinanceTestnetClient()
        authenticated_client = bot_wrapper.get_client()
    except ValueError as e:
        print(f"\n[CONFIGURATION ERROR] {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[CONNECTION ERROR] Failed to connect to the exchange: {str(e)}")
        sys.exit(1)

    place_future_orders(
        binance_client=authenticated_client,
        symbol=validated_inputs["symbol"],
        side=validated_inputs["side"],
        order_type=validated_inputs["type"],
        quantity=validated_inputs["quantity"],
        price=validated_inputs["price"],
        stop_price=validated_inputs.get("stop_price")
    )

if __name__ == "__main__":
    main()
