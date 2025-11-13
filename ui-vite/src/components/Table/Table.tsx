import { useCallback } from "react";
import type { Item } from "../../libs/Types.tsx";

interface TableProps {
    items: Item[];
    onRowClick: (item: Item) => void;
    sortBy?: "title" | "author" | "price";
    sortDir?: "asc" | "desc";
    onSortChange?: (column: "title" | "author" | "price") => void;
}

const Table = ({ items, onRowClick, sortBy, sortDir, onSortChange }: TableProps) => {
    const handleHeaderClick = useCallback(
        (col: "title" | "author" | "price") => {
            onSortChange?.(col);
        },
        [onSortChange]
    );

    const renderSortArrow = useCallback(
        (col: "title" | "author" | "price") =>
            sortBy === col ? (sortDir === "asc" ? "▲" : "▼") : null,
        [sortBy, sortDir]
    );

    return (
        <div className="container">
            <div className="table-responsive">
                <table
                    className="table table-striped table-bordered w-100"
                    style={{ tableLayout: "fixed", wordBreak: "break-word" }}
                >
                    <thead className="table-light">
                    <tr>
                        <th scope="col" style={{ width: "80px" }}>
                            Type
                        </th>
                        <th
                            scope="col"
                            role="button"
                            style={{ maxWidth: "250px" }}
                            className="text-truncate"
                            title="Sort by Title/Quote"
                            onClick={() => handleHeaderClick("title")}
                        >
                            Title / Quote {renderSortArrow("title")}
                        </th>
                        <th
                            scope="col"
                            role="button"
                            style={{ maxWidth: "200px" }}
                            className="text-truncate"
                            title="Sort by Author/Category"
                            onClick={() => handleHeaderClick("author")}
                        >
                            Author / Category {renderSortArrow("author")}
                        </th>
                        <th
                            scope="col"
                            role="button"
                            style={{ maxWidth: "150px" }}
                            className="text-truncate"
                            title="Sort by Price/Tags"
                            onClick={() => handleHeaderClick("price")}
                        >
                            Price / Tags {renderSortArrow("price")}
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    {items.map((item) => (
                        <tr key={item.id} onClick={() => onRowClick(item)} style={{ cursor: "pointer" }}>
                            <td style={{ width: "80px" }}>{item.type}</td>
                            <td style={{ maxWidth: "250px" }} className="text-truncate" title={item.type === "book" ? item.title : item.text}>
                                {item.type === "book" ? item.title : item.text}
                            </td>
                            <td style={{ maxWidth: "200px" }} className="text-truncate" title={item.type === "book" ? item.category : item.author}>
                                {item.type === "book" ? item.category : item.author}
                            </td>
                            <td style={{ maxWidth: "150px" }} className="text-truncate" title={item.type === "book" ? `£${item.price}` : item.tags?.join(", ")}>
                                {item.type === "book" ? `£${item.price}` : item.tags?.join(", ")}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Table;
