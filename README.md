# BookSearcher

Это бот с крутым 😎 backend'ом.

## Стэк

- Python
  - Aiogram
  - Aiogram-Dialog
  - Aiohttp
  - Requests
  - BS4
  - concurrent
- JavaScript (TypeScript)
  - Nest.JS
    - Swagger
  - PrismaORM
- Redis
- ElasticSearch

## Компоненты

### [Backend](backend/README.md)

Задачи:

- Взаимодействие с ElasticSearch
- Взаимодействие с PostgreSQL
- Предоставление документаций к API через Swagger

### [Bot](bot/README.md)

Задачи:

- Поиск книг по ключевым словам
- Отдача в красивом виде
- Взаимдоействие с backend

### [Scraper](scraper/README.md)

Задачи:

- Парсит [сайт](https://www.rulit.me) который предоставляет книги.
- Отдает данные в backend и elasticsearch.
