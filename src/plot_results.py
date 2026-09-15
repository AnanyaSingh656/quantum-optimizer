import csv
import matplotlib.pyplot as plt


def load_results(filename):
    data = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data.append(row)

    return data


def plot_gate_count(data):
    benchmarks = [row["benchmark"] for row in data]

    original = [
        int(row["original_gate_count"])
        for row in data
    ]

    optimized = [
        int(row["optimized_gate_count"])
        for row in data
    ]

    qiskit = [
        int(row["qiskit_gate_count"])
        for row in data
    ]

    x = range(len(benchmarks))
    width = 0.25

    plt.figure(figsize=(10, 6))

    plt.bar(
        [i - width for i in x],
        original,
        width=width,
        label="Original"
    )

    plt.bar(
        x,
        optimized,
        width=width,
        label="Our Optimizer"
    )

    plt.bar(
        [i + width for i in x],
        qiskit,
        width=width,
        label="Qiskit"
    )

    plt.xticks(list(x), benchmarks)
    plt.xlabel("Benchmark")
    plt.ylabel("Gate Count")
    plt.title("Gate Count Comparison")
    plt.legend()
    plt.tight_layout()

    plt.savefig("results/gate_count_comparison.png")
    plt.show()


def plot_weighted_cost(data):
    benchmarks = [row["benchmark"] for row in data]

    original = [
        int(row["original_weighted_cost"])
        for row in data
    ]

    optimized = [
        int(row["optimized_weighted_cost"])
        for row in data
    ]

    qiskit = [
        int(row["qiskit_weighted_cost"])
        for row in data
    ]

    x = range(len(benchmarks))
    width = 0.25

    plt.figure(figsize=(10, 6))

    plt.bar(
        [i - width for i in x],
        original,
        width=width,
        label="Original"
    )

    plt.bar(
        x,
        optimized,
        width=width,
        label="Our Optimizer"
    )

    plt.bar(
        [i + width for i in x],
        qiskit,
        width=width,
        label="Qiskit"
    )

    plt.xticks(list(x), benchmarks)
    plt.xlabel("Benchmark")
    plt.ylabel("Weighted Cost")
    plt.title("Weighted Cost Comparison")
    plt.legend()
    plt.tight_layout()

    plt.savefig("results/weighted_cost_comparison.png")
    plt.show()


if __name__ == "__main__":
    results = load_results(
        "results/benchmark_results.csv"
    )

    plot_gate_count(results)
    plot_weighted_cost(results)

    print("Graphs saved successfully!")