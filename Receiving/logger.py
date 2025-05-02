import logging
import os
from datetime import datetime

def setup_logger():
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_filename = os.path.join(log_dir, f"SMSReceivingLog_{datetime.now().strftime('%Y_%m_%d')}.txt")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
