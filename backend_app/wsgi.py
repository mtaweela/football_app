import os
from app.index import app

os.environ.setdefault("SETTINGS_MODULE", "app.settings")

application = app
