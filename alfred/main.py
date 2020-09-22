from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from alfred.api import router as api_router
from alfred.core.config import PROJECT_NAME, WEBHOOK_SECRET_TOKEN
from alfred.db.db_utils import close_postgres_connection, connect_to_postgres

app = FastAPI(title=PROJECT_NAME, docs_url=None, redoc_url=None)
app.add_event_handler("startup", connect_to_postgres)
app.add_event_handler("shutdown", close_postgres_connection)
app.include_router(api_router)


@app.middleware("http")
async def check_webhook_secret_token(request: Request, call_next):
    if WEBHOOK_SECRET_TOKEN and "/webhook/" in request.url.path:
        if request.query_params.get("token") != WEBHOOK_SECRET_TOKEN:
            return Response()
    return await call_next(request)
