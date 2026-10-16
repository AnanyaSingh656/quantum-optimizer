import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # save charts to files only (no window), so no warnings
import matplotlib.pyplot as plt


# Number of circuits shown in each chart
CIRCUITS_PER_GRAPH = 5

# Folders (outside src)
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
PLOTS_DIR = RESULTS_DIR / "plots"


def load_results(filename):
    data = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data.append(row)

    return data


def split_into_groups(data, size=CIRCUITS_PER_GRAPH):
    """
    Split the rows into groups of `size` circuits:
        39 circuits -> groups of 5, 5, 5, 5, 5, 5, 5, 4
    """

    return [data[i:i + size] for i in range(0, len(data), size)]


def plot_metric(data, metric, label, filename):
    """
    Grouped bar chart for one group of circuits:
    Original vs Our Optimizer vs Qiskit for the given metric
    (metric is "gate_count" or "weighted_cost").
    """

    benchmarks = [row["benchmark"] for row in data]

    original = [int(row[f"original_{metric}"]) for row in data]
    optimized = [int(row[f"optimized_{metric}"]) for row in data]
    qiskit = [int(row[f"qiskit_{metric}"]) for row in data]

    x = range(len(benchmarks))
    width = 0.25

    plt.figure(figsize=(10, 6))

    bars = [
        plt.bar([i - width for i in x], original, width=width, label="Original"),
        plt.bar(x, optimized, width=width, label="Our Optimizer"),
        plt.bar([i + width for i in x], qiskit, width=width, label="Qiskit"),
    ]

    # Show the value on top of every bar
    for bar_group in bars:
        plt.bar_label(bar_group, fontsize=8, padding=2)

    plt.xticks(list(x), benchmarks)
    plt.xlabel("Benchmark")
    plt.ylabel(label)
    plt.title(f"{label} Comparison ({benchmarks[0]} to {benchmarks[-1]})")
    plt.legend()
    plt.margins(y=0.12)
    plt.tight_layout()

    plt.savefig(filename)
    plt.close()


def plot_gate_count(data, filename):
    plot_metric(data, "gate_count", "Gate Count", filename)


def plot_weighted_cost(data, filename):
    plot_metric(data, "weighted_cost", "Weighted Cost", filename)


def plot_all(data):
    """
    Make one gate-count chart and one weighted-cost chart for every
    group of CIRCUITS_PER_GRAPH circuits. Returns the list of files saved.
    """

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Remove charts from an earlier run (e.g. if there were more circuits)
    for old_file in PLOTS_DIR.glob("*_part_*.png"):
        old_file.unlink()

    saved = []

    for part, group in enumerate(split_into_groups(data), start=1):
        gate_file = PLOTS_DIR / f"gate_count_part_{part}.png"
        cost_file = PLOTS_DIR / f"weighted_cost_part_{part}.png"

        plot_gate_count(group, gate_file)
        plot_weighted_cost(group, cost_file)

        print(f"Part {part}: {group[0]['benchmark']} to {group[-1]['benchmark']}")
        saved += [gate_file, cost_file]

    return saved


if __name__ == "__main__":
    results = load_results(
        RESULTS_DIR / "benchmark_results.csv"
    )

    saved_files = plot_all(results)

    print(f"Graphs saved successfully! ({len(saved_files)} files in {PLOTS_DIR})")
