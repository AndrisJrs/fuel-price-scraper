import os
import logging

log_level = os.environ.get('LOG_LEVEL', 'INFO')

logging.basicConfig(level=log_level)
