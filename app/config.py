import os
from dotenv import load_dotenv

load_dotenv()

PROXYAPI_API_KEY = os.getenv("PROXYAPI_API_KEY", "")
PROXYAPI_BASE_URL = os.getenv("PROXYAPI_BASE_URL", "https://api.proxyapi.ru/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
DB_PATH = os.getenv("DB_PATH", "data/supportpulse.db")
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "10"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
