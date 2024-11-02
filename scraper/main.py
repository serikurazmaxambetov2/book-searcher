import json
import logging
import os
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_max_page() -> int:
    """Получает максимальное количество страниц в сайте"""
    response = requests.get("https://www.rulit.me/books")
    soup = BeautifulSoup(response.text, "lxml")

    max_page_el = soup.select_one('a[title="Последняя страница"]')

    # https://www.rulit.me/books/all/84667/date
    max_page_url: str = max_page_el.get("href")  # type: ignore

    max_page = int(re.search(r"\d+", max_page_url).group())  # type: ignore
    return max_page


def get_book_links_by_page(page: int, proxies: Optional[Dict[str, str]] = None):
    """
    Получает ссылки на все книги которые находятся в текущей странице
    """
    response = requests.get(
        f"https://www.rulit.me/books/all/{page}/date", proxies=proxies
    )
    soup = BeautifulSoup(response.text, "lxml")

    book_links_raw = soup.select(".col-lg-9  h4 a")
    book_links: List[str] = []

    for book_link_raw in book_links_raw:
        link: str = book_link_raw.get("href")  # type: ignore
        book_links.append(link)

    return book_links


def get_book_by_link(link: str, proxies: Optional[Dict[str, str]] = None):
    """Получает название, описание книги по его ссылке"""
    response = requests.get(link, proxies=proxies)
    soup = BeautifulSoup(response.text, "lxml")

    title = soup.select_one(".col-md-12 h2").text  # type: ignore

    description_el = soup.select_one(".annotation p")
    for br in description_el.select("br"):  # type: ignore
        br.replace_with("\n")
    descriprtion = description_el.get_text().strip()  # type: ignore

    return {"title": title, "description": descriprtion}


def get_page_books(page: int, proxies: Optional[Dict[str, str]] = None):
    """Получаем все данные о книгах текущей страницы"""
    page_books = []

    book_links = get_book_links_by_page(page, proxies)
    for book_link in book_links:
        book = get_book_by_link(book_link, proxies)
        page_books.append(book)

        logger.info(f"[Книга]: {book.get('title')}")

    return page_books


def save_page_books(page: int, books: List[Dict[str, str]]):
    """Сохраняем книги постранично"""
    with open(f"pages/{page}.json", "w") as file:
        json.dump(books, file, indent=2, ensure_ascii=False)


def load_books_from_pages():
    """Получаем все книги из pages/*"""
    books = []

    for file in os.listdir("pages"):
        with open("pages/" + file, "r") as file:
            books += json.load(file)

    return books


def save_books(books: List[Dict[str, str]]):
    """Сохраняем все книги в scraped.json"""
    with open("scraped.json", "w") as file:
        json.dump(books, file, indent=2, ensure_ascii=False)


def main():
    max_page = get_max_page()

    # Парсим каждую страницу
    for page in range(1, max_page + 1):
        logger.info(f"[Страница {page}]")

        page_books = get_page_books(page)
        save_page_books(page, page_books)

        logger.info(f"Сохранили контент в файл pages/{page}.json")

    # Получаем все книги и сохраняем в общий файл
    books = load_books_from_pages()
    save_books(books)

    logger.info("Парсинг окончен")
    logger.info(f"Количество книг: {len(books)}")


########################### Многопоточный парсинг ###########################
def load_proxies() -> List[str]:
    """Получаем список проксей"""
    with open("proxies.txt", "r") as file:
        content = file.read()
        return content.split("\n")


PROXIES = load_proxies()


def scrape_page(page: int):
    try:
        logger.info(f"[Страница {page}]")
        proxy = random.choice(PROXIES)
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

        # Сохраняем книги текущей страницы
        page_books = get_page_books(page, proxies)
        save_page_books(page, page_books)

        logger.info(f"Сохранили контент в pages/{page}.json")
    except Exception:
        # Если ошибка меняем прокси
        scrape_page(page)


def main_thread():
    max_page = get_max_page()

    # Максимальное количество потоков одновременно
    max_threads = int(sys.argv[1] or 5)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Запускаем задания для каждого `page` в пуле
        futures = [
            executor.submit(scrape_page, page) for page in range(1, max_page + 1)
        ]

        # Дожидаемся завершения всех потоков
        for future in as_completed(futures):
            future.result()

    books = load_books_from_pages()
    save_books(books)

    logger.info("Парсинг окончен")
    logger.info(f"Количество книг: {len(books)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if sys.argv[1]:
        main_thread()
    else:
        main()
