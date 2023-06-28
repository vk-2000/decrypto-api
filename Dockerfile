FROM python:3.8.17-slim-bookworm

# RUN apk --no-cache add curl

# RUN curl -sSL https://install.python-poetry.org | python3 -
RUN pip install poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev --no-root

COPY . .

CMD ["sh", "-c", "scripts/start.sh"]