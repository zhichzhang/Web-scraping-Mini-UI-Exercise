import { useState, useMemo, useEffect } from "react";
import Table from "./components/Table/Table";
import Filters from "./components/Filters/Filters";
import Chart from "./components/Chart/Chart";
import DetailPanel from "./components/Detail Panel/DetailPanel.tsx";
import type { Dataset, Item } from "./libs/Types.tsx";
import { loadData } from "./libs/LoadData.tsx";
import { ChevronLeft, ChevronRight } from "lucide-react";
import "./App.css";

const ITEMS_PER_PAGE = 20;

export default function App() {
    const [dataset, setDataset] = useState<Dataset | null>(null);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");
    const [filterCategory, setFilterCategory] = useState("");
    const [filterTag, setFilterTag] = useState("");
    const [selectedItem, setSelectedItem] = useState<Item | null>(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [sortBy, setSortBy] = useState<"title" | "author" | "price" | undefined>();
    const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");

    useEffect(() => {
        loadData()
            .then((data) => setDataset(data))
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    const filteredItems = useMemo(() => {
        if (!dataset) return [];
        return dataset.items.filter((item) => {
            const matchesSearch =
                "title" in item
                    ? item.title.toLowerCase().includes(search.toLowerCase())
                    : item.text.toLowerCase().includes(search.toLowerCase());
            const matchesCategory =
                !filterCategory || ("category" in item && item.category === filterCategory);
            const matchesTag =
                !filterTag || ("tags" in item && item.tags.includes(filterTag));
            return matchesSearch && matchesCategory && matchesTag;
        });
    }, [dataset, search, filterCategory, filterTag]);

    const sortedItems = useMemo(() => {
        if (!sortBy) return filteredItems;
        return [...filteredItems].sort((a, b) => {
            const valA = (a as any)[sortBy] ?? "";
            const valB = (b as any)[sortBy] ?? "";
            if (typeof valA === "number" && typeof valB === "number") {
                return sortDir === "asc" ? valA - valB : valB - valA;
            }
            return sortDir === "asc"
                ? String(valA).localeCompare(String(valB))
                : String(valB).localeCompare(String(valA));
        });
    }, [filteredItems, sortBy, sortDir]);

    const totalPages = Math.ceil(sortedItems.length / ITEMS_PER_PAGE);
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const paginatedItems = sortedItems.slice(startIndex, startIndex + ITEMS_PER_PAGE);

    const handlePrev = () => setCurrentPage((p) => Math.max(p - 1, 1));
    const handleNext = () => setCurrentPage((p) => Math.min(p + 1, totalPages));

    const handleSortChange = (col: "title" | "author" | "price") => {
        if (sortBy === col) {
            setSortDir(sortDir === "asc" ? "desc" : "asc");
        } else {
            setSortBy(col);
            setSortDir("asc");
        }
        setCurrentPage(1);
    };

    const handleSearch = (value: string) => {
        setSearch(value);
        setCurrentPage(1);
    };

    const handleCategoryChange = (value: string) => {
        setFilterCategory(value);
        setCurrentPage(1);
    };

    const handleTagChange = (value: string) => {
        setFilterTag(value);
        setCurrentPage(1);
    };

    if (loading || !dataset) {
        return (
            <div className="d-flex flex-column justify-content-center align-items-center vh-100 fade show">
                <div
                    className="spinner-border text-primary"
                    style={{ width: "4rem", height: "4rem" }}
                    role="status"
                >
                    <span className="visually-hidden">Loading...</span>
                </div>
                <p className="mt-3 fs-5 text-muted">Loading data...</p>
            </div>
        );
    }

    return (
        <div className="container py-4">
            <h1 className="text-center mb-4"><strong>Dashboard</strong></h1>

            <Filters
                categories={dataset.filters.categories}
                tags={dataset.filters.tags}
                selectedCategory={filterCategory}
                selectedTag={filterTag}
                onCategoryChange={handleCategoryChange}
                onTagChange={handleTagChange}
                search={search}
                onSearch={handleSearch}
            />

            <div className="d-flex flex-wrap gap-3 mb-4">
                <div className="flex-grow-1 min-w-250">
                    <Chart dataset={dataset} type="books" />
                </div>
                <div className="flex-grow-1 min-w-250">
                    <Chart dataset={dataset} type="quotes" />
                </div>
            </div>

            <div className="table-responsive">
                <Table
                    items={paginatedItems}
                    sortBy={sortBy}
                    sortDir={sortDir}
                    onSortChange={handleSortChange}
                    onRowClick={setSelectedItem}
                />
            </div>

            {totalPages > 1 && (
                <div className="d-flex flex-column align-items-center mb-3">
                    <div className="pagination d-flex align-items-center gap-3">
                        {currentPage === 1 && totalPages > 1 && (
                            <div className="d-flex align-items-center gap-2">
                                <span className="fw-medium">{currentPage}</span>
                                <button className="btn btn-outline-secondary btn-sm" onClick={handleNext}>
                                    <ChevronRight size={16} />
                                </button>
                            </div>
                        )}
                        {currentPage > 1 && currentPage < totalPages && (
                            <div className="d-flex align-items-center gap-2">
                                <button className="btn btn-outline-secondary btn-sm" onClick={handlePrev}>
                                    <ChevronLeft size={16} />
                                </button>
                                <span className="fw-medium">{currentPage}</span>
                                <button className="btn btn-outline-secondary btn-sm" onClick={handleNext}>
                                    <ChevronRight size={16} />
                                </button>
                            </div>
                        )}
                        {currentPage === totalPages && totalPages > 1 && (
                            <div className="d-flex align-items-center gap-2">
                                <button className="btn btn-outline-secondary btn-sm" onClick={handlePrev}>
                                    <ChevronLeft size={16} />
                                </button>
                                <span className="fw-medium">{currentPage}</span>
                            </div>
                        )}
                    </div>

                    <small className="text-muted mt-2">
                        Page {currentPage} of {totalPages}
                    </small>
                    <small className="text-muted">
                        {"Item "}{startIndex + 1} – {"Item "}{Math.min(startIndex + ITEMS_PER_PAGE, sortedItems.length)}
                    </small>
                </div>
            )}

            <DetailPanel item={selectedItem} onClose={() => setSelectedItem(null)} />
        </div>
    );
}
