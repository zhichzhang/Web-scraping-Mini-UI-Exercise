# src/pagination.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_books_category_next_page_url(html, current_url):
    soup = BeautifulSoup(html, "lxml")
    next_link = soup.select_one(".next a")
    if next_link:
        return urljoin(current_url, next_link['href'])
    return None

def get_quotes_next_page_url(html, current_url):
    soup = BeautifulSoup(html, "lxml")
    next_li = soup.select_one("ul.pager li.next a")
    if next_li and next_li.get("href"):
        next_url = next_li['href'].strip()
        return urljoin(current_url, next_url)
    return None
