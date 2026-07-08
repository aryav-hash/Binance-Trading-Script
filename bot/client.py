import os
import logging
from dotenv import load_dotenv
from binance.client import Client

logger = logging.getLogger(__name__)

class BinanceTestnetClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")

        logger.info("Making connection to Binance ....")

        self.client = Client(api_key, api_secret, testnet=True)
        self.client.API_URL = "https://testnet.binancefuture.com"

        logger.info("Connected to the Binance Future Testnet.")

    def get_client(self):
        return self.client