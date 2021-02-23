FROM python:3.7

RUN pip install poetry 

COPY pyproject.toml .

RUN poetry install --no-dev

COPY . .

CMD poetry run gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker src.api.server:app
