from decouple import config
import os

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGER_CONFIG_FILE = os.path.join(BASE_DIR, "logging.yml")
