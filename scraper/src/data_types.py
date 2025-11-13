# src/data_types.py
from dataclasses import dataclass, field
from typing import List, Optional, Literal, Union

# Book item

@dataclass
class BookItem:
    id: str
    type: Literal["book"]
    title: str
    price: float
    availability: str
    rating: int
    category: str
    product_url: str

# Quote Item

@dataclass
class AuthorDetails:
    id: str
    url: str
    name: Optional[str] = None
    born_date: Optional[str] = None
    born_location:Optional[str] = None
    description: Optional[str] = None


@dataclass
class QuoteItem:
    id: str
    type: Literal["quote"]
    text: str
    author: str
    tags: List[str]
    page_url: str
    author_details: Optional[AuthorDetails] = None


# Summary aggregations

@dataclass
class CategoryCount:
    category: str
    count: int


@dataclass
class RatingCount:
    rating: int
    count: int


@dataclass
class TagCount:
    tag: str
    count: int


@dataclass
class AuthorCount:
    author: str
    count: int


@dataclass
class SummaryData:
    books_by_category: List[CategoryCount] = field(default_factory=list)
    books_by_rating: List[RatingCount] = field(default_factory=list)
    quotes_by_tag: List[TagCount] = field(default_factory=list)
    quotes_by_author: List[AuthorCount] = field(default_factory=list)


# Top-level dataset

@dataclass
class MetaInfo:
    dataset: str
    generated_at: str  # ISO timestamp
    total_items: int


@dataclass
class Filters:
    categories: List[str]
    tags: List[str]


Item = Union[BookItem, QuoteItem]


@dataclass
class Dataset:
    meta: MetaInfo
    filters: Filters
    items: List[Item]
    summary: SummaryData
