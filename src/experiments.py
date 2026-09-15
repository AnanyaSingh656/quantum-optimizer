import csv
from pathlib import Path

from .benchmarks import get_all_benchmarks
from .optimizer import cancel_with_commutation, cancel_inverse_gates
from .metrics import calculate_metrics
from .qiskit_baseline import optimize_with_qiskit
from .scheduler import schedule_independent_gates

def save_results_to_csv(results, filename):
    """
    Save benchmark results to a CSV file.
    """

    fieldnames = [
        "benchmark",
        "original_gate_count",
        "optimized_gate_count",
        "qiskit_gate_count",
        "original_depth",
        "optimized_depth",
        "qiskit_depth",
        "original_weighted_cost",
        "optimized_weighted_cost",
        "qiskit_weighted_cost",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)


def run_experiments():
    benchmarks = get_all_benchmarks()

    # Store all benchmark results here
    results = []

    for name, original_circuit in benchmarks.items():

        # Apply our optimizer
        commutation_circuit = cancel_with_commutation(
            original_circuit
        )

        optimized_circuit = cancel_inverse_gates(
            commutation_circuit
        )

        scheduled_circuit = schedule_independent_gates(
            optimized_circuit
        )  

        # Apply Qiskit's optimizer
        qiskit_circuit = optimize_with_qiskit(
            original_circuit
        )

        # Calculate metrics
        original_metrics = calculate_metrics(
            original_circuit
        )

        optimized_metrics = calculate_metrics(
            optimized_circuit
        )

        qiskit_metrics = calculate_metrics(
            qiskit_circuit
        )

        # Print results on terminal
        print("\n=========================================")
        print(f"Benchmark: {name}")
        print("=========================================")

        print("Original:", original_metrics)
        print("Our Optimizer:", optimized_metrics)
        print("Qiskit:", qiskit_metrics)

        # Add this benchmark's results to the CSV list
        results.append(
            {
                "benchmark": name,

                "original_gate_count": original_metrics["gate_count"],
                "optimized_gate_count": optimized_metrics["gate_count"],
                "qiskit_gate_count": qiskit_metrics["gate_count"],

                "original_depth": original_metrics["depth"],
                "optimized_depth": optimized_metrics["depth"],
                "qiskit_depth": qiskit_metrics["depth"],

                "original_weighted_cost": original_metrics[
                    "weighted_cost"
                ],
                "optimized_weighted_cost": optimized_metrics[
                    "weighted_cost"
                ],
                "qiskit_weighted_cost": qiskit_metrics[
                    "weighted_cost"
                ],
            }
        )

    # Create results folder if it does not exist
    results_folder = Path("results")
    results_folder.mkdir(exist_ok=True)

    # Save all results into CSV
    csv_filename = results_folder / "benchmark_results.csv"

    save_results_to_csv(results, csv_filename)

    print("\n=========================================")
    print("All benchmark results saved successfully!")
    print(f"CSV file: {csv_filename}")
    print("=========================================")


if __name__ == "__main__":
    run_experiments()