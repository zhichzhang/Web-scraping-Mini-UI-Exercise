# tests/test_pagination.py
import pytest
from src.pagination import get_books_category_next_page_url, get_quotes_next_page_url

def test_books_next_page_url():
    html_with_next = """
    <ul class="pager">
        <li class="next">
            <a href="/category/books/crime_51/page-2.html">Next</a>
        </li>
    </ul>
    """
    html_no_next = "<ul class='pager'></ul>"
    current_url = "https://books.toscrape.com/catalogue/category/books/crime_51/index.html"

    next_url = get_books_category_next_page_url(html_with_next, current_url)
    assert next_url == "https://books.toscrape.com/category/books/crime_51/page-2.html"

    last_page_url = get_books_category_next_page_url(html_no_next, current_url)
    assert last_page_url is None

def test_quotes_next_page_url():
    html_with_next = """
    <ul class="pager">
        <li class="next">
            <a href="/page/2/">Next</a>
        </li>
    </ul>
    """
    html_no_next = "<ul class='pager'></ul>"
    current_url = "https://quotes.toscrape.com/"

    next_url = get_quotes_next_page_url(html_with_next, current_url)
    assert next_url == "https://quotes.toscrape.com/page/2/"

    last_page_url = get_quotes_next_page_url(html_no_next, current_url)
    assert last_page_url is None
