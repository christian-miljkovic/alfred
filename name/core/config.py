import os
from databases import DatabaseURL

PROJECT_NAME = os.getenv("PROJECT_NAME", "name")
DATABASE_URL = DatabaseURL(os.getenv("DATABASE_URL"))
MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN")
