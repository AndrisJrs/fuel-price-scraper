import logging
import os

log_level = os.environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(level=log_level)
