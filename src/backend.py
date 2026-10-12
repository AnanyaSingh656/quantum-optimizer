
from .benchmarks import get_all_benchmarks
from .optimizer import cancel_with_commutation, cancel_inverse_gates
from .metrics import calculate_metrics
from .qiskit_baseline import optimize_with_qiskit


def get_benchmark_results(benchmark_name="mixed"):
    """Return JSON-compatible metrics for one benchmark."""

    benchmarks = get_all_benchmarks()

    if benchmark_name not in benchmarks:
        return {
            "status": "error",
            "message": f"Unknown benchmark: {benchmark_name}",
            "available_benchmarks": list(benchmarks.keys()),
        }

    original = benchmarks[benchmark_name]

    commutation_result = cancel_with_commutation(original)
    optimized = cancel_inverse_gates(commutation_result)
    qiskit_optimized = optimize_with_qiskit(original)

    return {
        "status": "success",
        "benchmark": benchmark_name,
        "results": {
            "original": calculate_metrics(original),
            "optimized": calculate_metrics(optimized),
            "qiskit": calculate_metrics(qiskit_optimized),
        },
    }
