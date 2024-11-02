import json
import logging
import os
import re
from typing import List

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


def get_book_links_by_page(page: int):
    """
    Получает ссылки на все книги которые находятся в текущей странице
    """
    response = requests.get(f"https://www.rulit.me/books/all/{page}/date")
    soup = BeautifulSoup(response.text, "lxml")

    book_links_raw = soup.select(".col-lg-9  h4 a")
    book_links: List[str] = []

    for book_link_raw in book_links_raw:
        link: str = book_link_raw.get("href")  # type: ignore
        book_links.append(link)

    return book_links


def get_book_by_link(link: str):
    """Получает название, описание книги по его ссылке"""
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")

    title = soup.select_one(".col-md-12 h2").text  # type: ignore

    description_el = soup.select_one(".annotation p")
    for br in description_el.select("br"):  # type: ignore
        br.replace_with("\n")
    descriprtion = description_el.get_text().strip()  # type: ignore

    return {"title": title, "description": descriprtion}


def main():
    max_page = get_max_page()

    # Парсим каждую страницу
    for page in range(1, max_page + 1):
        page_books = []

        logger.info(f"[Страница {page}]")

        # Получаем все данные о книгах текущей страницы
        book_links = get_book_links_by_page(page)
        for book_link in book_links:
            book = get_book_by_link(book_link)
            page_books.append(book)

            logger.info(f"[Книга]: {book.get('title')}")

        # Сохраняем книги постранично
        with open(f"pages/{page}.json", "w") as file:
            json.dump(page_books, file, indent=2, ensure_ascii=False)

        logger.info(f"Сохранили контент в файл pages/{page}.json")

    # Получаем все книги и сохраняем в общий файл
    books = []
    for file in os.listdir("pages"):
        with open("pages/" + file, "r") as file:
            books += json.load(file)

    with open("scraped.json", "w") as file:
        json.dump(books, file, indent=2, ensure_ascii=False)

    logger.info("Парсинг окончен")
    logger.info(f"Количество книг: {len(books)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
