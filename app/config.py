import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

load_dotenv('../.env', verbose=True)

ESV_API_KEY = os.getenv('ESV_API_KEY')
assert ESV_API_KEY