FROM python:3.7

ENV PYTHONUNBUFFERED=1 \
    PYTHONDEFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.3

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml ./


RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev --no-ansi

COPY . .
RUN rm -rf tests

ENV G_WORKERS=1 \
    G_THREADS=6 \
    G_PORT=8080 \
    G_LOG_LEVEL=info \
    G_KEEP_ALIVE=305

CMD alembic upgrade head && \
    gunicorn alfred.main:app --reload\
    -w ${G_WORKERS} \
    --threads ${G_THREADS} \
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:${G_PORT} \
    --log-config logging.conf \
    --log-level=${G_LOG_LEVEL} \
    --keep-alive=${G_KEEP_ALIVE}