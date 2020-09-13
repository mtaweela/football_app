from decouple import config
import os


DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGER_CONFIG_FILE = os.path.join(BASE_DIR, "logging.yml")


DB_SETTINGS = {
    "database": "football_app",
    "user": "user",
    "password": "db_pass",
    "host": "localhost",
    "port": 3306,
}