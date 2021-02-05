import os
from databases import DatabaseURL

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

PROJECT_NAME = os.getenv("PROJECT_NAME", "alfred")
DATABASE_URL = DatabaseURL(os.getenv("DATABASE_URL"))
MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN")
REACT_APP_URL = os.getenv("REACT_APP_URL")
RECOMMENDATION_APP_URL = os.getenv("RECOMMENDATION_APP_URL")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_ACCOUNT_SID_DEV = os.getenv("TWILIO_ACCOUNT_SID_DEV")
TWILIO_ACCOUNT_AUTH_TOKEN = os.getenv("TWILIO_ACCOUNT_AUTH_TOKEN")

FROM_PHONE_NUMBER = os.getenv("FROM_PHONE_NUMBER")
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")

TWILIO_ACCOUNT_MESSAGING_SID = os.getenv("TWILIO_ACCOUNT_MESSAGING_SID")
TWILIO_PHONE_NUMBER_SID = os.getenv("TWILIO_PHONE_NUMBER_SID")
