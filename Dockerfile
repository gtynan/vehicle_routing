FROM python:3.7

RUN pip install poetry 

WORKDIR /app

COPY pyproject.toml .

RUN poetry config virtualenvs.create false && \
    poetry install -v --no-interaction --no-ansi --no-dev

COPY . .

CMD gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker src.api.server:app
