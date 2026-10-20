import csv
from pathlib import Path

from .benchmarks import get_all_circuit_names, load_circuit
from .optimizer import optimize_circuit
from .metrics import calculate_metrics
from .qiskit_baseline import optimize_with_qiskit
from .scheduler import schedule_independent_gates
from .verify import check_equivalence

# Results folder (outside src)
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


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
        "rounds",
        "equivalent",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)


def run_experiments():
    # Every circuit file in the test_circuits folder (any number of circuits)
    circuit_names = get_all_circuit_names()

    # Store all benchmark results here
    results = []
    checked = 0
    passed = 0

    for name in circuit_names:

        original_circuit = load_circuit(name)

        # Apply our optimizer (round-wise, same as main.py)
        optimized_circuit, rounds = optimize_circuit(original_circuit)

        scheduled_circuit = schedule_independent_gates(
            optimized_circuit
        )

        # Apply Qiskit's optimizer
        qiskit_circuit = optimize_with_qiskit(
            original_circuit
        )

        # Calculate metrics
        original_metrics = calculate_metrics(original_circuit)
        optimized_metrics = calculate_metrics(optimized_circuit)
        qiskit_metrics = calculate_metrics(qiskit_circuit)

        # Check that the optimized circuit gives the same result
        check = check_equivalence(original_circuit, optimized_circuit)

        if check["equivalent"] is not None:
            checked += 1
            passed += int(check["equivalent"])

        # Print results on terminal
        print("\n=========================================")
        print(f"Benchmark: {name}")
        print("=========================================")

        print("Original:", original_metrics)
        print("Our Optimizer:", optimized_metrics)
        print("Qiskit:", qiskit_metrics)
        print(f"Rounds: {rounds}")
        print(f"Result check: {check['message']}")

        # Add this benchmark's results to the CSV list
        results.append(
            {
                "benchmark": Path(name).stem,

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

                "rounds": rounds,
                "equivalent": (
                    "not checked" if check["equivalent"] is None
                    else check["equivalent"]
                ),
            }
        )

    # Create results folder if it does not exist
    RESULTS_DIR.mkdir(exist_ok=True)

    # Save all results into CSV
    csv_filename = RESULTS_DIR / "benchmark_results.csv"

    save_results_to_csv(results, csv_filename)

    print("\n=========================================")
    print(f"Circuits run: {len(circuit_names)}")
    print(f"Result check: {passed}/{checked} optimized circuits "
          f"give the same result as the original")
    print("All benchmark results saved successfully!")
    print(f"CSV file: {csv_filename}")
    print("=========================================")


if __name__ == "__main__":
    run_experiments()
