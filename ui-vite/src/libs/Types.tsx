export type BookItem = {
    id: string;
    type: "book";
    title: string;
    price: number;
    availability: string;
    rating: number;
    category: string;
    product_url: string;
};

export type AuthorDetails = {
    id: string;
    url: string;
    name?: string;
    born_date?: string;
    born_location?: string;
    description?: string;
};

export type QuoteItem = {
    id: string;
    type: "quote";
    text: string;
    author: string;
    tags: string[];
    page_url: string;
    author_details?: AuthorDetails;
};

export type Item = BookItem | QuoteItem;

export type CategoryCount = { category: string; count: number };
export type RatingCount = { rating: number; count: number };
export type TagCount = { tag: string; count: number };
export type AuthorCount = { author: string; count: number };

export type SummaryData = {
    books_by_category: CategoryCount[];
    books_by_rating: RatingCount[];
    quotes_by_tag: TagCount[];
    quotes_by_author: AuthorCount[];
};

export type MetaInfo = { dataset: string; generated_at: string; total_items: number };
export type Filters = { categories: string[]; tags: string[] };

export type Dataset = {
    meta: MetaInfo;
    filters: Filters;
    items: Item[];
    summary: SummaryData;
};
