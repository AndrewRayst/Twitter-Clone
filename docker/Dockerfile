FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends gcc

WORKDIR /app

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY src .

CMD if [ "$FASTAPI_DEBUG" = "TRUE" ]; \
    then poetry run uvicorn main:application --host 0.0.0.0 --port 5000; \
    else poetry run uvicorn main:application --host 0.0.0.0 --port 5000; fi
