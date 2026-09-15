from .benchmarks import create_benchmark_circuit
from .optimizer import (
    cancel_with_commutation,
    cancel_inverse_gates,
)
from .metrics import calculate_metrics
from .report import print_comparison
from .qiskit_baseline import optimize_with_qiskit

def save_circuit(circuit, filename):
    """
    Save a circuit diagram into a text file.
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(circuit))

def main():
    original_circuit = create_benchmark_circuit()

    commutation_circuit = cancel_with_commutation(
        original_circuit
    )

    optimized_circuit = cancel_inverse_gates(
        commutation_circuit
    )

    qiskit_circuit = optimize_with_qiskit(original_circuit)
    
    save_circuit(
        original_circuit,
        "results/original_circuit.txt"
    )

    save_circuit(
        optimized_circuit,
        "results/optimized_circuit.txt"
    )

    original_metrics = calculate_metrics(original_circuit)
    optimized_metrics = calculate_metrics(optimized_circuit)
    qiskit_metrics = calculate_metrics(qiskit_circuit)


    print("Original Circuit:")
    print(original_circuit)

    print("\nOptimized Circuit:")
    print(optimized_circuit)

    print("\nOriginal Metrics:")
    print(original_metrics)

    print("\nOptimized Metrics:")
    print(optimized_metrics)

    print_comparison(original_metrics, optimized_metrics)

    print("\nQiskit's Optimized Metrics:")
    print(qiskit_metrics)

if __name__ == "__main__":
    main()