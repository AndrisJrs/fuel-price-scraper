import os
import logging

log_level = os.environ.get('LOG_LEVEL', 'WARNING')

logging.basicConfig(level=log_level)