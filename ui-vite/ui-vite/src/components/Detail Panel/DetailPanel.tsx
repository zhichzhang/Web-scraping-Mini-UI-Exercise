import React, { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { Item, BookItem } from "../../libs/Types.tsx";

interface DetailPanelProps {
    item: Item | null;
    onClose: () => void;
}

const DETAIL_PANEL_WIDTH = 500;

const DetailPanel: React.FC<DetailPanelProps> = ({ item, onClose }) => {
    const panelRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (panelRef.current && !panelRef.current.contains(event.target as Node)) {
                onClose();
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [onClose]);

    const renderStars = (rating: number) => {
        const fullStars = "★".repeat(Math.floor(rating));
        const emptyStars = "☆".repeat(5 - Math.floor(rating));
        return fullStars + emptyStars;
    };

    return (
        <AnimatePresence>
            {item && (
                <>
                    <motion.div
                        className="backdrop"
                        onClick={onClose}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 0.5 }}
                        exit={{ opacity: 0 }}
                        style={{
                            position: "fixed",
                            top: 0,
                            left: 0,
                            width: "100%",
                            height: "100%",
                            backgroundColor: "#000",
                            zIndex: 999,
                            cursor: "pointer",
                        }}
                    />

                    <motion.div
                        ref={panelRef}
                        initial={{ x: DETAIL_PANEL_WIDTH }}
                        animate={{ x: 0 }}
                        exit={{ x: DETAIL_PANEL_WIDTH }}
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        style={{
                            position: "fixed",
                            top: 0,
                            right: 0,
                            width: DETAIL_PANEL_WIDTH,
                            height: "100%",
                            backgroundColor: "#fff",
                            zIndex: 1000,
                            boxShadow: "-3px 0px 10px rgba(0,0,0,0.15)",
                            overflowY: "auto",
                            padding: "1rem",
                            display: "flex",
                            flexDirection: "column",
                        }}
                    >
                        <div className="d-flex justify-content-between align-items-center mb-3">
                            <h5 className="mb-0">
                                <strong>{item.type === "book" ? item.title : item.text}</strong>
                            </h5>
                            <button
                                type="button"
                                className="btn-close"
                                onClick={onClose}
                            ></button>
                        </div>

                        <div>
                            {item.type === "book" ? (
                                <div className="mb-3">
                                    <p>
                                        <strong>Category:</strong> {item.category}
                                    </p>
                                    <p>
                                        <strong>Price:</strong> £{item.price}
                                    </p>
                                    <p>
                                        <strong>Rating:</strong>{" "}
                                        <span style={{ color: "#f5c518" }}>
                                            {renderStars((item as BookItem).rating)}
                                        </span>
                                    </p>
                                    <p>
                                        <strong>Availability:</strong> {item.availability}
                                    </p>
                                    <p>
                                        <strong>Link:</strong>: <a
                                        href={item.product_url}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="link-primary"
                                    >
                                        Product link
                                    </a>
                                    </p>
                                </div>
                            ) : (
                                <div className="mb-3">
                                    <p>
                                        <strong>Author:</strong> {item.author} (<span>
                                            <a
                                                href={item.author_details?.url}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="link-primary">about</a>
                                        </span>)
                                    </p>
                                    <p>
                                        <strong>Tags:</strong> {item.tags.join(", ")}
                                    </p>
                                    <p>
                                        <strong>Link:</strong>: <a
                                        href={item.page_url}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="link-primary"
                                    >
                                        Quote page
                                    </a>
                                    </p>
                                    {item.author_details && (
                                        <>
                                            <p>
                                                <strong>Born:</strong> {item.author_details.born_date} in{" "}
                                                {item.author_details.born_location}
                                            </p>
                                            <p>
                                                <strong>Description:</strong> <br/>
                                                {item.author_details.description}
                                            </p>
                                        </>
                                    )}
                                </div>
                            )}
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
};

export default DetailPanel;
