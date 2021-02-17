FROM python:3.7

RUN pip install poetry 

COPY pyproject.toml .

RUN poetry install

COPY . .


CMD poetry run gunicorn --bind 8080 --workers 1 --worker-class uvicorn.workers.UvicornWorker src.api.server:app

