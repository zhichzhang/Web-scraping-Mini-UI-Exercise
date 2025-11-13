from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from datetime import datetime
import random
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import time

from tqdm import tqdm

from src.robots import can_fetch
from src.pagination import get_books_category_next_page_url, get_quotes_next_page_url

visited = set()
visited_lock = threading.Lock()

BASE_BOOKS_URL = "https://books.toscrape.com/"
BASE_QUOTES_URL = "https://quotes.toscrape.com/"

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def fetch_page(url, retries=3, delay_range=(0.5, 1.5)):
    with visited_lock:
        if url in visited:
            log(f"[SKIP] Already visited {url}")
            return None
        visited.add(url)

    if not can_fetch(url):
        log(f"[BLOCKED] robots.txt prevents fetching {url}")
        return None

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                time.sleep(random.uniform(0.5, 1.5))
                log(f"[OK] Fetched {url}")
                return resp.text
            else:
                log(f"[WARN] Status {resp.status_code} for {url}")
        except requests.RequestException as e:
            log(f"[ERROR] Attempt {attempt} failed for {url}: {e}")
            time.sleep(2 ** attempt * 0.5)  # exponential backoff

    log(f"[FAIL] Could not fetch {url} after {retries} attempts")
    return None

def get_books_category_urls():
    html = fetch_page(BASE_BOOKS_URL)
    if not html:
        return {}

    soup = BeautifulSoup(html, "lxml")
    categories = {}
    for a in soup.select(".side_categories ul ul li a"):
        name = a.get_text(strip=True)
        url = urljoin(BASE_BOOKS_URL, a['href'])
        categories[name] = url
    return categories

def extract_book_links_from_page(url, html):
    soup = BeautifulSoup(html, "lxml")
    return [urljoin(url, a['href']) for a in soup.select("article.product_pod h3 a")]

def fetch_books_in_category(category_name, category_url, max_pages=500):
    book_links = []
    url = category_url
    page_count = 0

    while url:
        if max_pages and page_count >= max_pages:
            log(f"[STOP] Reached max pages for {category_name}")
            break

        html = fetch_page(url)
        if not html:
            break

        book_links.extend(extract_book_links_from_page(url, html))
        url = get_books_category_next_page_url(html, url)
        page_count += 1

    log(f"[DONE] Fetched {len(book_links)} books from {category_name}")
    return {category_name: list(set(book_links))}  # dedup

def fetch_all_books_parallel(max_workers=10):
    categories = get_books_category_urls()
    all_books = {}

    log(f"Found {len(categories)} categories: {list(categories.keys())}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_books_in_category, name, url): name for name, url in categories.items()}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching categories"):
            category_name = futures[future]
            try:
                result = future.result()
                if result:
                    for cat, links in result.items():
                        if cat in all_books:
                            all_books[cat].extend(links)
                        else:
                            all_books[cat] = links
            except Exception as e:
                log(f"[ERROR] Fetching category {category_name}: {e}")

    # Final dedup
    for cat in all_books:
        all_books[cat] = list(set(all_books[cat]))

    log("Finished fetching all categories.")
    return all_books

def fetch_all_quotes_pages_parallel(max_workers=10, max_pages=1000):
    urls = []
    url = BASE_QUOTES_URL
    page_count = 0
    pbar = tqdm(desc="Fetching quote pages", unit="page")

    while url:
        if max_pages and page_count >= max_pages:
            log(f"[STOP] Reached max pages for quotes")
            break

        html = fetch_page(url)
        if not html:
            log(f"[FAIL] Failed to fetch {url}")
            break

        urls.append(url)
        page_count += 1
        url = get_quotes_next_page_url(html, url)
        pbar.update(1)

    pbar.close()
    log(f"Total quote pages fetched: {len(urls)}")
    return urls

if __name__ == "__main__":
    all_quotes_pages = fetch_all_quotes_pages_parallel(max_workers=10)
    log(f"Found {len(all_quotes_pages)} quotes pages in total.")
    log(all_quotes_pages)
