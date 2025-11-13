import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from fetcher import fetch_all_books_parallel, fetch_all_quotes_pages_parallel
from parser import parse_book_page, parse_quotes_from_a_page
from data_types import BookItem, SummaryData, CategoryCount, RatingCount, Dataset, MetaInfo, Filters, QuoteItem, TagCount, AuthorCount
import json
from pathlib import Path
from datetime import datetime, timezone

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")


def get_output_path():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path = Path(f"data/{timestamp}/dataset.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def fetch_and_parse_books(max_workers=10, limit=None):
    log("Fetching book URLs...")
    book_pages_dict = fetch_all_books_parallel(max_workers)

    urls_to_parse = []  # list of (url, category)
    for category, urls in book_pages_dict.items():
        for url in urls:
            urls_to_parse.append((url, category))
            if limit and len(urls_to_parse) >= limit:
                break
        if limit and len(urls_to_parse) >= limit:
            break

    log(f"Parsing {len(urls_to_parse)} book pages...")
    books = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_book_page, url, category) for url, category in urls_to_parse]
        for future in as_completed(futures):
            book = future.result()
            if book:
                books.append(book)

    log(f"Parsed {len(books)} books.")
    return books


def fetch_and_parse_quotes_pages(max_workers=10, limit=None):
    all_quotes_urls = fetch_all_quotes_pages_parallel(max_workers=max_workers)
    all_quotes = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(parse_quotes_from_a_page, url): url for url in all_quotes_urls}

        for future in as_completed(futures):
            if limit and len(all_quotes) >= limit:
                break

            page_url = futures[future]
            quotes = future.result()
            if quotes:
                remaining = limit - len(all_quotes) if limit else None
                if remaining:
                    quotes = quotes[:remaining]
                all_quotes.extend(quotes)

            if limit and len(all_quotes) >= limit:
                break

    log(f"Parsed {len(all_quotes)} quotes from up to {len(all_quotes_urls)} pages.")
    return all_quotes


def build_summary(books, quotes=None):
    quotes = quotes or []

    category_counts = {}
    rating_counts = {}

    for book in books:
        category_counts[book.category] = category_counts.get(book.category, 0) + 1
        rating_counts[book.rating] = rating_counts.get(book.rating, 0) + 1

    tag_counts = {}
    author_counts = {}

    for quote in quotes:
        author_counts[quote.author] = author_counts.get(quote.author, 0) + 1
        for tag in quote.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    return SummaryData(
        books_by_category=[CategoryCount(category=k, count=v) for k, v in category_counts.items()],
        books_by_rating=[RatingCount(rating=k, count=v) for k, v in rating_counts.items()],
        quotes_by_tag=[TagCount(tag=k, count=v) for k, v in tag_counts.items()],
        quotes_by_author=[AuthorCount(author=k, count=v) for k, v in author_counts.items()]
    )


def build_dataset(books, quotes=None):
    quotes = quotes or []
    items = books + quotes
    summary = build_summary(books, quotes)
    return Dataset(
        meta=MetaInfo(
            dataset="books_and_quotes",
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_items=len(items)
        ),
        filters=Filters(
            categories=list({b.category for b in books}),
            tags=list({t for q in quotes for t in q.tags})
        ),
        items=items,
        summary=summary
    )


def save_dataset(dataset, path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(dataset, f, default=lambda o: o.__dict__, ensure_ascii=False, indent=2)
    log(f"Saved dataset to {path}")

    items_path = Path("data/items.jsonl")
    items = getattr(dataset, "items", [])

    with items_path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, default=lambda o: o.__dict__, ensure_ascii=False) + "\n")
    log(f"Saved {len(items)} items to {items_path}")


def main():
    output_path = get_output_path()
    books = fetch_and_parse_books(limit=2)
    quotes = fetch_and_parse_quotes_pages(limit=2)
    dataset = build_dataset(books, quotes)
    save_dataset(dataset, output_path)


if __name__ == "__main__":
    main()
