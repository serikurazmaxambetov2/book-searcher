FROM python:3.11

ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .
CMD sleep 30 && poetry run python startup.py
