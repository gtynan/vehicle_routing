FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY . .

ENV PORT=8080

CMD poetry run uvicorn src.api.server:app --reload --port $PORT
