FROM python:3.7

RUN pip install poetry 

COPY pyproject.toml .

RUN poetry install

EXPOSE ${PORT}

COPY . .

CMD poetry run uvicorn src.api.server:app --host 0.0.0.0 --port $PORT
