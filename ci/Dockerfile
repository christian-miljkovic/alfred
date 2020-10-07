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
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD alembic upgrade head && pytest --cov=alfred tests/