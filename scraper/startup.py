import json
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import requests

# Получаем URL для взаимодействия с сервером из переменной окружения
BACKEND_URL: str = os.getenv("BACKEND_URL")  # type: ignore


def is_server_first_running():
    """
    Проверяет, есть ли уже данные на сервере, отправляя GET-запрос к первому элементу.
    Если сервер возвращает статус 404, предполагается, что данных еще нет,
    и можно загружать новые данные (избегая дублирования при перезагрузке контейнера Docker).
    """
    response = requests.get(BACKEND_URL + "/book/1")  # type: ignore
    return response.status_code == 404


def send_book(book: Dict[str, str]) -> None:
    """
    Отправляет книгу на сервер с помощью POST-запроса.
    """
    requests.post(BACKEND_URL + "/book/", json=book)


def load_books():
    """
    Загружает книги из JSON-файла `scraped.json`.
    """
    with open("scraped.json", "r") as file:
        return json.load(file)


def main():
    """
    Основная функция программы. Проверяет, есть ли уже данные на сервере,
    загружает список книг и отправляет их на сервер с использованием пула потоков.
    """
    # Проверяем, если данных на сервере нет, тогда выполняем загрузку
    if not is_server_first_running():
        return None

    # Загружаем книги из файла
    books = load_books()
    max_threads = 100  # Устанавливаем максимальное количество потоков

    # Используем пул потоков для параллельной отправки книг
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for book in books:
            # Отправляем каждую книгу в отдельном потоке
            executor.submit(send_book, book)


# Запускаем программу, если файл выполняется напрямую
if __name__ == "__main__":
    main()
