from qiskit import transpile


def optimize_with_qiskit(circuit):
    """
    Optimize the circuit using Qiskit's
    built-in optimization pass manager.
    """

    optimized_circuit = transpile(
        circuit,
        optimization_level=3
    )

    return optimized_circuit