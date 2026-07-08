import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_dir = "logs"
    log_filename = "trading_bot.log"
    log_filepath = os.path.join(log_dir, log_filename)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_format = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    file_handler = RotatingFileHandler(
        log_filepath,
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    logging.getLogger("urllib3").setLevel(logging.WARNING)