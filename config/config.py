import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
API_KEY = os.getenv("API_KEY")

API_URL = os.getenv(
    "API_URL",
    "https://www.alphavantage.co/query"
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "etl_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "logs"


RAW_DATA_FILE = RAW_DATA_DIR / "raw_stock_data.json"

PROCESSED_DATA_FILE = (
    PROCESSED_DATA_DIR / "processed_stock_data.csv"
)


for directory in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    LOG_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)


print("Configuration loaded successfully!")
