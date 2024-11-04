# Scraper

## Стэк

- Python
- Requests
- BS4
- Многопоточность | Однопоточность

## Запуск

> [!NOTE]
> Вам не обязательно запустить парсер т.к. данные уже спаршены (scraped.json). Но для теста вы можете запустить его.

Чтобы запустить в однопоточном режиме:

```bash
poetry run python main.py
```

В многопоточном режиме:
сначала требуется создать proxies.txt

```bash
poetry run python main.py {количество потоков}
```

Пример:

```bash
poetry run python main.py 10
```

Это запустит парсер в 10 потоков

## Заливка данных на backend и elasticsearch:

Чтобы залить данные в backend и elasticsearch просто запустите файл startup.py.

```bash
poetry run python startup.py
```

Этот скрипт работает в многопоточном режимe (100 потоков).
Перед заливкой проверяет данные на backend чтобы не было дупликатов
