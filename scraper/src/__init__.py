# src/__init__.py

# ----------------------------
# Fetching
# ----------------------------
from .fetcher import (
    fetch_all_books_parallel,
    fetch_all_quotes_pages_parallel,
    fetch_page,
)

# ----------------------------
# Pagination helpers
# ----------------------------
from .pagination import (
    get_books_category_next_page_url,
    get_quotes_next_page_url,
)

# ----------------------------
# Parsing / processing
# ----------------------------
from .parser import (
    parse_all_books,
    parse_book_page,
    parse_quotes_from_a_page,
    get_author_details,
    generate_unique_id,
)

# ----------------------------
# Robots.txt helper
# ----------------------------
from .robots import can_fetch

# ----------------------------
# Types
# ----------------------------
from .data_types import (
    BookItem,
    QuoteItem,
    AuthorDetails,
    CategoryCount,
    RatingCount,
    TagCount,
    AuthorCount,
    SummaryData,
    MetaInfo,
    Filters,
    Dataset,
    Item,
)

# ----------------------------
# Define __all__ for cleaner imports
# ----------------------------
__all__ = [
    # fetcher
    "fetch_all_books_parallel",
    "fetch_all_quotes_pages_parallel",
    "fetch_page",
    # pagination
    "get_books_category_next_page_url",
    "get_quotes_next_page_url",
    # parser/paster
    "parse_all_books",
    "parse_book_page",
    "parse_quotes_from_a_page",
    "get_author_details",
    "generate_unique_id",
    # robots
    "can_fetch",
    # types
    "BookItem",
    "QuoteItem",
    "AuthorDetails",
    "CategoryCount",
    "RatingCount",
    "TagCount",
    "AuthorCount",
    "SummaryData",
    "MetaInfo",
    "Filters",
    "Dataset",
    "Item",
]
