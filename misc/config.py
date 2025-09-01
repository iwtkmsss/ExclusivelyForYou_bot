from pathlib import Path
from database import Database
from dotenv import load_dotenv

import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

TOKEN = os.getenv('BOT_TOKEN')

DEFAULT_PHOTO_FOR_RECIPE = "https://global-web-assets.cpcdn.com/assets/blank-fd7d144d8ce163db654e5a02c40b08a2775adb7897d16e4062681dc7e1b2800f.png"
db_file = Path(BASE_DIR, "misc", 'db.sqlite')

BDB = Database(db_file)
