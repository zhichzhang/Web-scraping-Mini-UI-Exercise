interface FilterProps {
    categories: string[];
    tags: string[];
    selectedCategory: string;
    selectedTag: string;
    onCategoryChange: (value: string) => void;
    onTagChange: (value: string) => void;
    search: string;
    onSearch: (value: string) => void;
}

const Filters = ({
                     categories,
                     tags,
                     selectedCategory,
                     selectedTag,
                     onCategoryChange,
                     onTagChange,
                     search,
                     onSearch,
                 }: FilterProps) => {
    return (
        <div className="container mb-3">
            <div className="row g-2">
                <div className="col-12 col-md-6 col-lg-8">
                    <input
                        type="text"
                        className="form-control w-100"
                        placeholder="Search title/quote..."
                        value={search}
                        onChange={(e) => onSearch(e.target.value)}
                    />
                </div>

                <div className="col-6 col-md-3 col-lg-2">
                    <select
                        className="form-select w-100"
                        value={selectedCategory}
                        onChange={(e) => onCategoryChange(e.target.value)}
                    >
                        <option value="">All Categories</option>
                        {categories.map((c) => (
                            <option key={c} value={c}>
                                {c}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="col-6 col-md-3 col-lg-2">
                    <select
                        className="form-select w-100"
                        value={selectedTag}
                        onChange={(e) => onTagChange(e.target.value)}
                    >
                        <option value="">All Tags</option>
                        {tags.map((t) => (
                            <option key={t} value={t}>
                                {t}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
        </div>
    );
};

export default Filters;
