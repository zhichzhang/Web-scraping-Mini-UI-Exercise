# Web scraping + Mini-UI Exercise

## How to run?

### **Scraper (Python)**

- **Install dependencies**:

```shell
# If you have requirements.txt
pip install -r requirements.txt
```

- **Run the scraper**:

```shell
python src/main.py
```

- **Output**
  - This generates dataset in `data/<timestamp>/dataset.json` and `data/items.jsonl`. 

### **UI-Vite (React+TypeScript+Vite)**

- **Install dependencies**:

```shell
npm install
```

- **Start development server**:

```shell
npm run dev
```

- **Open in browser**:
  - Typically at `http://localhost:5173` (or whatever Vite/CRA outputs)
  - The app automatically loads `items.jsonl` or the served JSON.
- **Usage in UI**:
  - Search/filter books or quotes.
  - Sort by price/rating (Books) or author/tag count (Quotes).
  - Click a row to open a sidebar with detailed information.
  - Charts show category/tag distributions.
  - Pagination allows navigating 20 items per page.
  - Pop up a detail panel showing the scraped fields when a table row is clicked, and close it either by clicking the close button or anywhere outside the panel. 

## Design Decisions

### Scraper

- **Parallel Fetching**
  - Used `ThreadPoolExecutor` to fetch multiple book/quote pages concurrently.
  - Supports optional limits for testing or partial scraping.
- **Parsing**
  - Extracts relevant fields:
    - Books: title, price, rating, category, availability, product URL.
    - Quotes: text, author, tags, author details (born date/location, bio).
  - Generates unique IDs for each item.
- **Data Cleaning**
  - Fixes garbled text in author details or locations.
  - Safely handles missing author info.
- **Aggregation**
  - Precomputes counts for:
    - Books by category & rating
    - Quotes by tag & author
  - Supports charts and summaries on the frontend.
- **Output**
  - `dataset.json` includes metadata, filters, items, summary.
  - `items.jsonl` allows incremental reading.
  - Each run saves to a timestamped folder for versioning.
- **Performance & Safety**
  - Concurrent parsing improves speed.
  - Logging tracks progress.
  - Robust parsing avoids crashes on malformed pages.

### UI-Vite

- **Data Loading and Structure**
  - **Strict Types & Dataset:** Defined TypeScript types (`BookItem`, `QuoteItem`, `Item`) to ensure type safety and clarity.
  - **Single Source (items.jsonl):** Only `items.jsonl` is used for incremental loading on the frontend.
  - **Handle Messy Data:** Preprocessed and cleaned any garbled or inconsistent fields before rendering.
- **Frontend Architecture**
  - **React Functional Components with Hooks:** Used `useState`, `useEffect`, `useMemo`, `useCallback` for state and performance optimization.
  - **Component Breakdown:**
    - **App:** Main container orchestrating state and rendering.
    - **Filters:** Handles search, category, and tag filters.
    - **Table:** Sortable and paginated display of items.
    - **Chart:** Tiny visualizations for summaries.
    - **DetailPanel:** Off-canvas sidebar showing item details on row click.
  - **Bootstrap Integration:** Responsive layout with grid, forms, tables, and offcanvas component.
  - **Client-side Pagination:** 20 items per page with intuitive navigation (`<-`, current, `->`) handled entirely on the frontend.
- **Table & Interactivity**
  - **Sorting:** Clickable table headers allow sorting by title, author, or price for books, and by author/tag counts for quotes. Sorting resets to page 1.
  - **Pagination:** Buttons above the table reflect current page and position in dataset.
  - **Detail Panel:**
    - Pops up as an off-canvas sidebar on row click.
    - Displays scraped fields like title, author, price, rating, category, tags, and author details.
    - Dismissable by clicking outside or pressing the close button.
    - Uses `motion.div` for smooth slide-in/slide-out animations. 
- **Visualization**
  - **Tiny Charts:** Placed between header and table, summarizing counts (books by category/rating, quotes by tag/author).
  - **Chart.js:** Chosen for simplicity and responsive integration with React.
- **User Experience**
  - **Responsive Layout:** Filters, table, and charts adapt to different screen sizes using Bootstrap.
  - **Search Emphasis:** Larger search bar for usability.
  - **Detail Panel UX:** Slide-in sidebar with natural click-away dismissal.
  - **Loading Indicator:** Spinner shown while dataset is being loaded.
- **Performance & Scalability**
  - **Client-side Operations:** Sorting, filtering, and pagination are all handled locally for instant updates.
  - **Memoization:** `useMemo` and `useCallback` reduce unnecessary recalculations and re-renders.

## What I will do if I have more time?

- **Enhanced Filtering & Search**
  - Add multi-select filters for categories and tags.
  - Implement fuzzy search or search-as-you-type for faster results.
- **Advanced Pagination & Sorting**
  - Infinite scroll or virtualized table for large datasets.
  - Multi-column sorting (e.g., sort by rating then price).
- **Improved Detail Panel**
  - Add tabs or sections for better organization of book/author/quote details.
  - Include images or author portraits if available.
  - Add animations or transitions for smoother UX with `motion.div`.
- **Better Visualizations**
  - Interactive charts with tooltips and filtering.
  - Mini sparklines inside the table for quick insight.
- **Performance & Responsiveness**
  - Lazy load table rows and charts for very large datasets.
  - Add caching to reduce repeated data processing.
- **Accessibility & UX**
  - Keyboard navigation for table and detail panel.
  - Dark mode or theme toggle.
- **Testing & Reliability**
  - Add unit and integration tests for table, filters, and detail panel.
  - Add error handling and fallback UI if `items.jsonl` fails to load.

## Limitations

- **Client-side Pagination & Sorting:** All operations—including filtering, sorting, and pagination—are performed in the browser. For very large datasets, this may affect performance.

- **Static Data Source:** The frontend only consumes `items.jsonl`; there is no live backend or incremental updates. Any new data requires re-running the scraper and reloading the JSON.

- **Security & Production Considerations:** Currently, there is no authentication, rate-limiting, or other security measures. For production deployment, additional safeguards would be necessary.

- **UI & Accessibility:** While the interface uses Bootstrap and is mostly responsive, some layouts may be cramped on very small screens. Accessibility for keyboard navigation and screen readers is limited.

- **Data Quality: **The app handles messy or inconsistent scraped data, but malformed or missing fields may still cause minor UI glitches.