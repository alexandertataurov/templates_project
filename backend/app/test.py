# test_env.py
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ENV_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
logger.debug("Loading .env from: %s", ENV_FILE_PATH)
load_dotenv(dotenv_path=ENV_FILE_PATH, verbose=True)
logger.debug("SECRET_KEY=%s", os.getenv("SECRET_KEY"))
logger.debug("DATABASE_URL=%s", os.getenv("DATABASE_URL"))
