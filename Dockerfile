FROM python:3.9-slim

RUN pip install poetry

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY . .

EXPOSE 8000

CMD [ "poetry", "run",  "uvicorn", "src.api.server:app", "--reload", "--workers", "1", "--host",  "0.0.0.0", "--port", "8000" ]
