FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends gcc

WORKDIR /app

COPY alembic alembic
COPY alembic.ini .

COPY poetry.lock .
COPY pyproject.toml .

RUN python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev,test --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY static static
COPY src src

CMD if [ "$FASTAPI_DEBUG" = "TRUE" ]; \
    then uvicorn src.main:application --host 0.0.0.0 --port 5000; \
    else gunicorn src.main:application --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000; fi