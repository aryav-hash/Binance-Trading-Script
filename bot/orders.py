import time
import logging
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)

def place_future_orders(binance_client, symbol: str, side: str, order_type: str, quantity: float, price: float | None = None, stop_price: float | None = None):
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    order_params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity
    }

    if order_type in ['LIMIT', 'STOP']:
        if not price:
            raise ValueError(f"A target price must be specified for {order_type} orders.")
        order_params['price'] = price
        order_params['timeInForce'] = 'GTC'

    if order_type == 'STOP':
        if not stop_price:
            raise ValueError("A stop price is requested for STOP orders.")
        order_params['stopPrice'] = stop_price

    print("\n" + "=" * 45)
    print("  ORDER REQUEST SUMMARY  ")
    print("=" * 4)
    print(f"  Asset Pair:  {symbol}")
    print(f"  Action Side: {side}")
    print(f"  Order Type:  {order_type}")
    print(f"  Size/Quantity: {quantity}")
    if order_type in ['LIMIT', 'STOP']:
        print(f"  Target Price: {price}")
    if order_type == 'STOP':
        print(f"  Stop Price:  {stop_price}")
    print("=" * 45)

    logger.info(f"Sending order payload to Binance Futures API: {order_params}")

    try:
        response = binance_client.futures_create_order(**order_params)
        order_id = response.get('orderId') or response.get('algoId') or response.get('clientOrderId', 'UNKNOWN')
        logger.info(f"Order successfully placed. Raw API Response: {response}")

        if order_type == 'MARKET':
            print("[System] Waiting 2 seconds for exchange matching engine.... ")
            time.sleep(2)
            response = binance_client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            logger.info(f"Order updated. New Response: {response}")
        
        status = response.get('status')
        executed_qty = response.get('executedQty', '0.0')
        avg_price = response.get('avgPrice', '0.0')

        if avg_price == '0' or avg_price == '0.0':
            avg_price = response.get('price', 'N/A')
        
        print("\n[SUCCESS] Order successfully transacted on Testnet!")
        print("-" * 45)
        print("         ORDER RESPONSE DETAILS         ")
        print("-" * 45)
        print(f"  Order ID:  {order_id}")
        print(f"  Status:    {status}")
        print(f"  Executed Quantity: {executed_qty}")
        print(f"  Avg Price: {avg_price}")
        print("=" * 45 + "\n")
        
        return response
    
    except BinanceAPIException as e:
        error_summary = f"Binance API Rejection | Code: {e.code} | Message: {e.message}"
        logger.error(error_summary)

        print("\n[FAILURE] Order rejected by Binance Futures Testnet Engine.")
        print("-" * 45)
        print(f" Reason: {e.message}")
        print("=" * 45 + "\n")
        return None
    
    except Exception as e:
        error_summary = f"System runtime or communication failure: {str(e)}"
        logger.error(error_summary)
        print("\n[FAILURE] An unexpected systemic error occurred.")
        print("-" * 45)
        print(f"  Details: {str(e)}")
        print("=" * 45 + "\n")
        return None

