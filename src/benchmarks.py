from qiskit import QuantumCircuit


def create_benchmark_circuit():
    """
    Original mixed benchmark circuit.
    """

    circuit = QuantumCircuit(3)

    # Adjacent cancellation
    circuit.h(0)
    circuit.h(0)

    # Commutation cancellation
    circuit.x(1)
    circuit.h(0)
    circuit.h(0)

    # Non-cancellable pattern
    circuit.h(2)
    circuit.x(2)
    circuit.h(2)

    # Two-qubit gates
    circuit.cx(0, 1)
    circuit.cx(1, 2)

    # T and T-dagger cancellation
    circuit.t(0)
    circuit.tdg(0)

    # SWAP gate
    circuit.swap(1, 2)

    return circuit


def create_adjacent_cancellation_circuit():
    """
    Benchmark with adjacent cancellable gates.
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.h(0)

    circuit.x(1)
    circuit.x(1)

    return circuit


def create_commutation_circuit():
    """
    Benchmark with gates separated by operations
    on a different qubit.
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.x(1)
    circuit.h(0)

    return circuit


def create_inverse_gate_circuit():
    """
    Benchmark with inverse gate pairs.
    """

    circuit = QuantumCircuit(2)

    circuit.t(0)
    circuit.tdg(0)

    circuit.s(1)
    circuit.sdg(1)

    return circuit


def create_two_qubit_circuit():
    """
    Benchmark containing two-qubit gates.
    """

    circuit = QuantumCircuit(3)

    circuit.cx(0, 1)
    circuit.cx(0, 1)

    circuit.swap(1, 2)

    return circuit

def get_all_benchmarks():
    """
    Return all benchmark circuits.
    """

    return {
        "mixed": create_benchmark_circuit(),
        "adjacent": create_adjacent_cancellation_circuit(),
        "commutation": create_commutation_circuit(),
        "inverse_gates": create_inverse_gate_circuit(),
        "two_qubit": create_two_qubit_circuit(),
    }