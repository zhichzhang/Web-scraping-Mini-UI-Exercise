import { useMemo } from "react";
import type { Dataset } from "../../libs/Types.tsx";
import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    type ChartData,
    type ChartOptions,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface ChartProps {
    dataset: Dataset;
    type: "books" | "quotes";
}

const Chart = ({ dataset, type }: ChartProps) => {
    const accentHSL = getComputedStyle(document.documentElement)
        .getPropertyValue("--accent-hsl")
        .trim();

    const { labels, dataCounts, chartTitle } = useMemo(() => {
        if (type === "books") {
            return {
                labels: dataset.summary.books_by_category.map((b) => b.category),
                dataCounts: dataset.summary.books_by_category.map((b) => b.count),
                chartTitle: "Books by Category",
            };
        } else {
            return {
                labels: dataset.summary.quotes_by_tag.map((q) => q.tag),
                dataCounts: dataset.summary.quotes_by_tag.map((q) => q.count),
                chartTitle: "Quotes by Tag",
            };
        }
    }, [dataset, type]);

    const data: ChartData<"bar"> = useMemo(
        () => ({
            labels,
            datasets: [
                {
                    label: chartTitle,
                    data: dataCounts,
                    backgroundColor: `hsl(${accentHSL})`,
                    hoverBackgroundColor: `hsl(${accentHSL} / 0.8)`,
                },
            ],
        }),
        [labels, dataCounts, chartTitle, accentHSL]
    );

    const maxLabelsVisible = 10;
    const rotateLabels = labels.length > maxLabelsVisible;

    const options: ChartOptions<"bar"> = useMemo(
        () => ({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" },
                title: {
                    display: true,
                    text: chartTitle,
                    font: { size: 24, weight: "bold" },
                    color: "#333",
                },
                tooltip: { enabled: true },
            },
            layout: { padding: 10 },
            scales: {
                x: {
                    ticks: {
                        autoSkip: rotateLabels,
                        maxRotation: rotateLabels ? 45 : 0,
                        minRotation: rotateLabels ? 30 : 0,
                        callback: function (val) {
                            const label = this.getLabelForValue(val as number) as string;
                            return label.length > 15 ? label.slice(0, 15) + "…" : label;
                        },
                    },
                },
                y: { beginAtZero: true },
            },
        }),
        [chartTitle, rotateLabels]
    );

    return (
        <div className="container mb-4 overflow-auto">
            <div className="w-100" style={{ minWidth: "400px", height: "350px" }}>
                <Bar data={data} options={options} />
            </div>
        </div>
    );
};

export default Chart;
