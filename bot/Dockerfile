FROM python:3.11

WORKDIR /bot

# Установка Poetry
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Установка зависимостей
COPY package.lock pyproject.toml ./
RUN poetry install 

# Копирование проекта
COPY . .

# Запуск
CMD poetry run python main.py
