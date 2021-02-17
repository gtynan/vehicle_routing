FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY . .

CMD poetry run gunicorn --bind :$PORT src.api.server:app -w 1 -k uvicorn.workers.UvicornWorker
