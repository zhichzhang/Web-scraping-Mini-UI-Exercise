import threading
from datetime import datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid

from src.robots import can_fetch
from src.types import BookItem, QuoteItem, AuthorDetails
import re

_id_lock = threading.Lock()
_used_ids = set()
_author_lock = threading.Lock()
_author_cache = {}

BASE_QUOTES = "https://quotes.toscrape.com/"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def generate_unique_id(prefix):
    """Generate a globally unique ID with prefix, thread-safe."""
    while True:
        new_id = f"{prefix}-{uuid.uuid4()}" if prefix else str(uuid.uuid4())
        with _id_lock:
            if new_id not in _used_ids:
                _used_ids.add(new_id)
                return new_id

def get_author_details(author_href):
    """Return AuthorDetails for a given author URL, fetching if not cached."""
    author_url = urljoin(BASE_QUOTES, author_href)

    with _author_lock:
        if author_url in _author_cache:
            return _author_cache[author_url]

    if not can_fetch(author_url):
        log(f"[BLOCKED] robots.txt prevents fetching {author_url}")
        # Optionally return a minimal AuthorDetails
        author = AuthorDetails(id=str(uuid.uuid4()), url=author_url)
        with _author_lock:
            _author_cache[author_url] = author
        return author

    try:
        resp = requests.get(author_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        name_el = soup.select_one("h3.author-title")
        born_date_el = soup.select_one("span.author-born-date")
        born_loc_el = soup.select_one("span.author-born-location")
        desc_el = soup.select_one("div.author-description")

        born_location = None
        if born_loc_el:
            text = born_loc_el.get_text(strip=True)
            if text.lower().startswith("in "):
                text = text[3:]
            born_location = text

        author = AuthorDetails(
            id=f"author-{uuid.uuid4()}",
            url=author_url,
            name=name_el.get_text(strip=True) if name_el else None,
            born_date=born_date_el.get_text(strip=True) if born_date_el else None,
            born_location=born_location,
            description=desc_el.get_text(strip=True) if desc_el else None
        )

        with _author_lock:
            _author_cache[author_url] = author

        return author

    except requests.RequestException as e:
        log(f"[ERROR] Failed to fetch author page {author_url}: {e}")
        author = AuthorDetails(id=str(uuid.uuid4()), url=author_url)
        with _author_lock:
            _author_cache[author_url] = author
        return author

def convert_rating(classes):
    """Convert 'star-rating One/Two/Three...' to integer"""
    ratings_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for cls in classes:
        if cls in ratings_map:
            return ratings_map[cls]
    return 0

def parse_book_page(url, category, html=None):
    try:
        if html is None:
            # Always fetch if no HTML is provided
            if not can_fetch(url):
                print(f"[BLOCKED] {url} blocked by robots.txt")
                return None
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html = response.text

        if html is None:
            log(f"[ERROR] No HTML to parse for {url}")
            return None

        soup = BeautifulSoup(html, "lxml")

        title_tag = soup.select_one("div.product_main h1")
        title = title_tag.text.strip() if title_tag else ""

        price_tag = soup.select_one(".price_color")
        price = float(re.sub(r"[^0-9.]", "", price_tag.text)) if price_tag else 0.0

        avail_tag = soup.select_one(".availability")
        availability = avail_tag.text.strip() if avail_tag else ""

        rating_tag = soup.select_one("p.star-rating")
        rating = convert_rating(rating_tag["class"]) if rating_tag else 0

        if category is None:
            breadcrumb_items = soup.select("ul.breadcrumb li a")
            if len(breadcrumb_items) >= 2:
                category = breadcrumb_items[-1].get_text(strip=True)
            else:
                category = "Unknown"

        return BookItem(
            id=generate_unique_id("book"),
            type="book",
            title=title,
            price=price,
            availability=availability,
            rating=rating,
            category=category,
            product_url=url
        )

    except Exception as e:
        log(f"Error parsing {url}: {e}")
        return None


def parse_all_books(book_pages_dict, max_workers=10):
    """Parse all book pages concurrently using ThreadPoolExecutor"""
    books_items = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for category, urls in book_pages_dict.items():
            for url in urls:
                futures.append(executor.submit(parse_book_page, url, category))

        for future in as_completed(futures):
            book = future.result()
            if book:
                books_items.append(book)

    return books_items

def parse_quotes_from_a_page(page_url, html=None):
    try:
        if html is None:
            if not can_fetch(page_url):
                log(f"[BLOCKED] {page_url} blocked by robots.txt")
                return []

            import requests
            resp = requests.get(page_url, timeout=10)
            resp.raise_for_status()
            html = resp.text

        if html is None:
            log(f"[ERROR] No HTML to parse for {page_url}")
            return []

        soup = BeautifulSoup(html, "lxml")
    except Exception as e:
        log(f"Failed to parse {page_url}: {e}")
        return []

    quotes = []

    for div in soup.select("div.quote"):
        text_el = div.select_one("span.text")
        author_el = div.select_one("small.author")
        tags_el = div.select("div.tags a.tag")
        about_link_el = div.select_one("span a[href]")

        if text_el and author_el and about_link_el:
            author_details = get_author_details(about_link_el['href'])
            quotes.append(
                QuoteItem(
                    id=generate_unique_id("quote"),
                    type="quote",
                    text=text_el.get_text(strip=True).strip("“”"),
                    author=author_el.get_text(strip=True),
                    tags=[a.get_text(strip=True) for a in tags_el],
                    page_url=page_url,
                    author_details=author_details
                )
            )

    return quotes


if __name__ == "__main__":
    book_pages_dict = {
        'Womens Fiction': [
            'https://books.toscrape.com/catalogue/the-devil-wears-prada-the-devil-wears-prada-1_243/index.html'
        ],
        'Music': [
            'https://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html'
        ]
    }
    all_books = parse_all_books(book_pages_dict)

    for book in all_books:
        log(book)
    quotes = parse_quotes_from_a_page("https://quotes.toscrape.com/")
    for quote in quotes:
        log(quote)
