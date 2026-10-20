from pathlib import Path

from .benchmarks import get_all_circuit_names, load_circuit
from .optimizer import optimize_circuit
from .metrics import calculate_metrics
from .qiskit_baseline import optimize_with_qiskit
from .verify import check_equivalence


def _find_circuit_name(benchmark_name):
    """
    Accept "circuit_1.qasm" or just "circuit_1" and return the file name,
    or None if no such circuit exists in test_circuits.
    """

    available = get_all_circuit_names()

    if benchmark_name in available:
        return benchmark_name

    for name in available:
        if Path(name).stem == benchmark_name:
            return name

    return None


def get_benchmark_results(benchmark_name="circuit_1.qasm"):
    """Return JSON-compatible metrics for one circuit in test_circuits."""

    circuit_name = _find_circuit_name(benchmark_name)

    if circuit_name is None:
        return {
            "status": "error",
            "message": f"Unknown benchmark: {benchmark_name}",
            "available_benchmarks": get_all_circuit_names(),
        }

    original = load_circuit(circuit_name)

    optimized, rounds = optimize_circuit(original)
    qiskit_optimized = optimize_with_qiskit(original)

    check = check_equivalence(original, optimized)

    return {
        "status": "success",
        "benchmark": circuit_name,
        "rounds": rounds,
        "equivalent": check["equivalent"],
        "results": {
            "original": calculate_metrics(original),
            "optimized": calculate_metrics(optimized),
            "qiskit": calculate_metrics(qiskit_optimized),
        },
    }


def get_all_benchmark_results():
    """Return the results for every circuit in test_circuits."""

    return [
        get_benchmark_results(name)
        for name in get_all_circuit_names()
    ]
