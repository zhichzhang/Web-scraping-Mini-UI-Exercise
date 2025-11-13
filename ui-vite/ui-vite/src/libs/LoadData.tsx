import type { Dataset, Item, CategoryCount, RatingCount, TagCount, AuthorCount } from "./Types.tsx";

function fixGarbled(text: string): string {
    return text
        .replace(/â/g, "’")
        .replace(/â€“/g, "–")
        .replace(/â€”/g, "—")
        .replace(/â€œ/g, "“")
        .replace(/â€�/g, "”");
}

export async function loadData(): Promise<Dataset> {
    const res = await fetch("/data/items.jsonl");
    const text = await res.text();

    const items: Item[] = text
        .split("\n")
        .filter((line) => line.trim() !== "")
        .map((line) => {
            const item = JSON.parse(line) as Item;

            if (item.type === "book") {
                item.title = fixGarbled(item.title);
                item.category = fixGarbled(item.category);
            } else if (item.type === "quote") {
                item.text = fixGarbled(item.text);
                item.author = fixGarbled(item.author);
                if (item.tags) {
                    item.tags = item.tags.map(fixGarbled);
                }
                if (item.author_details) {
                    item.author_details.born_location = fixGarbled(item.author_details.born_location ?? "");
                    item.author_details.description = fixGarbled(item.author_details.description ?? "");
                }
            }

            return item;
        });

    const books = items.filter((i) => i.type === "book");
    const quotes = items.filter((i) => i.type === "quote");

    const booksByCategory: CategoryCount[] = Array.from(
        new Set(books.map((b) => b.category))
    ).map((category) => ({
        category,
        count: books.filter((b) => b.category === category).length,
    }));

    const booksByRating: RatingCount[] = Array.from(
        new Set(books.map((b) => b.rating))
    ).map((rating) => ({
        rating,
        count: books.filter((b) => b.rating === rating).length,
    }));

    const quotesByTag: TagCount[] = Array.from(
        new Set(quotes.flatMap((q) => q.tags))
    ).map((tag) => ({
        tag,
        count: quotes.filter((q) => q.tags.includes(tag)).length,
    }));

    const quotesByAuthor: AuthorCount[] = Array.from(
        new Set(quotes.map((q) => q.author))
    ).map((author) => ({
        author,
        count: quotes.filter((q) => q.author === author).length,
    }));

    const dataset: Dataset = {
        meta: {
            dataset: "books_and_quotes",
            generated_at: new Date().toISOString(),
            total_items: items.length,
        },
        filters: {
            categories: Array.from(new Set(books.map((b) => b.category))),
            tags: Array.from(new Set(quotes.flatMap((q) => q.tags))),
        },
        items,
        summary: {
            books_by_category: booksByCategory,
            books_by_rating: booksByRating,
            quotes_by_tag: quotesByTag,
            quotes_by_author: quotesByAuthor,
        },
    };

    return dataset;
}
