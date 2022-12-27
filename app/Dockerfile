FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /app/

RUN pip install --upgrade pip
COPY poetry.lock pyproject.toml /app/

ARG POETRY_ARGS="--only main --no-interaction --no-ansi"
RUN pip install poetry && poetry install $POETRY_ARGS
COPY . /app/
RUN chmod +x start.sh
