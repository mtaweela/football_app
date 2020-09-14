from os import environ, getenv, path


DEBUG = False
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

LOGGER_CONFIG_FILE = path.join(BASE_DIR, "logging.yml")

DB_SETTINGS = {
    "database": environ.get("MYSQL_DATABASE", "football_app"),
    "user": environ.get("MYSQL_USER", "root"),
    "password": environ.get("MYSQL_PASSWORD", ""),
    "host": environ.get("DB_HOST", "localhost"),
    "port": int(environ.get("DB_PORT", "3306")),
}
