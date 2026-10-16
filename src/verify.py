from qiskit.quantum_info import Operator, Statevector


# Building the full matrix of a circuit takes memory that doubles with
# every qubit, so the full check is only done up to this many qubits.
MAX_QUBITS_FOR_CHECK = 10


def check_equivalence(original_circuit, optimized_circuit):
    """
    Check that the optimized circuit gives the same result as the original.

    Returns a dictionary:
        "equivalent"         True / False, or None if the circuit is too big
        "same_unitary"       the two circuits are the same quantum operation
                             (same result for every possible input state)
        "same_statevector"   same output state when starting from |00..0>
    """

    if original_circuit.num_qubits > MAX_QUBITS_FOR_CHECK:
        return {
            "equivalent": None,
            "same_unitary": None,
            "same_statevector": None,
            "message": (
                f"Not checked: more than {MAX_QUBITS_FOR_CHECK} qubits"
            ),
        }

    # equiv() ignores a global phase, which cannot be measured
    same_unitary = Operator(original_circuit).equiv(
        Operator(optimized_circuit)
    )

    same_statevector = Statevector.from_instruction(original_circuit).equiv(
        Statevector.from_instruction(optimized_circuit)
    )

    equivalent = same_unitary and same_statevector

    return {
        "equivalent": equivalent,
        "same_unitary": same_unitary,
        "same_statevector": same_statevector,
        "message": "Equivalent" if equivalent else "NOT equivalent",
    }
