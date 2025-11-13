# from .parser import parse_books_page, parse_quotes_page
from dataclasses import asdict
from pathlib import Path
from src import parse_book_page, parse_quotes_from_a_page


def test_parse_books_page():
  # Load the fixture
  html = Path("./fixtures/sample_book_page.html").read_text(encoding="utf-8")

  # Call parser with HTML
  book = parse_book_page(
    url="https://books.toscrape.com/catalogue/the-long-shadow-of-small-ghosts-murder-and-memory-in-an-american-city_848/index.html",
    category=None,
    html=html
  )

  # Expected data (adjust fields to match your fixture)
  expected = {
    "type": "book",
    "title": "The Long Shadow of Small Ghosts: Murder and Memory in an American City",
    "price": 10.97,
    "availability": "In stock (15 available)",
    "rating": 1,
    "category": "Crime",
    "product_url": "https://books.toscrape.com/catalogue/the-long-shadow-of-small-ghosts-murder-and-memory-in-an-american-city_848/index.html"
  }

  # Check all fields except 'id'
  for key, value in expected.items():
    assert getattr(book, key) == value



def test_parse_quotes_from_a_page():
    html = Path("./fixtures/sample_quote_page.html").read_text(encoding="utf-8")
    quotes = parse_quotes_from_a_page("https://quotes.toscrape.com/", html)

    assert quotes, "No quotes were parsed"
    quotes_dicts = [asdict(q) for q in quotes]

    for q in quotes_dicts:
      q.pop("id", None)
      q.pop("author_details", None)

    true_quotes = [
      {
        "type": "quote",
        "text": "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.",
        "author": "Albert Einstein",
        "tags": ["change", "deep-thoughts", "thinking", "world"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "It is our choices, Harry, that show what we truly are, far more than our abilities.",
        "author": "J.K. Rowling",
        "tags": ["abilities", "choices"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.",
        "author": "Albert Einstein",
        "tags": ["inspirational", "life", "live", "miracle", "miracles"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.",
        "author": "Jane Austen",
        "tags": ["aliteracy", "books", "classic", "humor"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "Imperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.",
        "author": "Marilyn Monroe",
        "tags": ["be-yourself", "inspirational"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "Try not to become a man of success. Rather become a man of value.",
        "author": "Albert Einstein",
        "tags": ["adulthood", "success", "value"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "It is better to be hated for what you are than to be loved for what you are not.",
        "author": "André Gide",
        "tags": ["life", "love"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "I have not failed. I've just found 10,000 ways that won't work.",
        "author": "Thomas A. Edison",
        "tags": ["edison", "failure", "inspirational", "paraphrased"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "A woman is like a tea bag; you never know how strong it is until it's in hot water.",
        "author": "Eleanor Roosevelt",
        "tags": ["misattributed-eleanor-roosevelt"],
        "page_url": "https://quotes.toscrape.com/"
      },
      {
        "type": "quote",
        "text": "A day without sunshine is like, you know, night.",
        "author": "Steve Martin",
        "tags": ["humor", "obvious", "simile"],
        "page_url": "https://quotes.toscrape.com/"
      }
    ]

    for parsed, true in zip(quotes_dicts, true_quotes):
      assert parsed == true, f"Mismatch in quote: {parsed['text']}"