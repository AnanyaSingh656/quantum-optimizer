"""
Gate knowledge used by the optimizer.

This file only answers questions about gates; it never changes a circuit.
  - matrix_to_gate(matrix): which single gate equals this 2x2 matrix?
  - gates_commute(...):     can these two gates swap places safely?
  - are_inverses(...):      do these two gates cancel each other?
"""

import numpy as np


# ---------------------------------------------------------------- matrices

_S2 = 1 / np.sqrt(2)

SINGLE_QUBIT_MATRICES = {
    "h":   np.array([[_S2, _S2], [_S2, -_S2]], dtype=complex),
    "x":   np.array([[0, 1], [1, 0]], dtype=complex),
    "y":   np.array([[0, -1j], [1j, 0]], dtype=complex),
    "z":   np.array([[1, 0], [0, -1]], dtype=complex),
    "s":   np.array([[1, 0], [0, 1j]], dtype=complex),
    "sdg": np.array([[1, 0], [0, -1j]], dtype=complex),
    "t":   np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex),
    "tdg": np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]], dtype=complex),
}

IDENTITY = np.eye(2, dtype=complex)

# Single-qubit gates the merging pass is allowed to combine and output
MERGEABLE_GATES = set(SINGLE_QUBIT_MATRICES)


def _same_up_to_global_phase(a, b):
    """
    True if a = e^(i*phase) * b. A global phase cannot be measured, so the
    two operations give exactly the same results.
    """

    # For 2x2 unitaries: |trace(a^dagger b)| == 2 exactly when a ~ b
    return abs(abs(np.trace(a.conj().T @ b)) - 2) < 1e-9


def matrix_to_gate(matrix):
    """
    Return:
        "id"        if the matrix is the identity (the gates can be removed)
        gate name   if the matrix equals one gate, e.g. "z"
        None        if no single gate in our gate set matches
    """

    if _same_up_to_global_phase(matrix, IDENTITY):
        return "id"

    for name, gate_matrix in SINGLE_QUBIT_MATRICES.items():
        if _same_up_to_global_phase(matrix, gate_matrix):
            return name

    return None


def product_of_gates(gate_names):
    """
    Matrix of applying gate_names in order (first gate is applied first).
    """

    result = IDENTITY
    for name in gate_names:
        result = SINGLE_QUBIT_MATRICES[name] @ result
    return result


# ---------------------------------------------------------------- inverses

# Gate -> the gate that undoes it
INVERSE_OF = {
    "h": "h", "x": "x", "y": "y", "z": "z",
    "s": "sdg", "sdg": "s",
    "t": "tdg", "tdg": "t",
    "cx": "cx", "cz": "cz", "swap": "swap",
}

# Two-qubit gates whose qubit order does not matter
SYMMETRIC_GATES = {"cz", "swap"}


def are_inverses(name_a, qubits_a, name_b, qubits_b):
    """
    True if gate b exactly undoes gate a (so a followed by b does nothing).
    qubits_* are tuples of qubit indices, e.g. (0, 1) for CX control 0, target 1.
    """

    if INVERSE_OF.get(name_a) != name_b:
        return False

    if name_a in SYMMETRIC_GATES:
        return set(qubits_a) == set(qubits_b)

    return tuple(qubits_a) == tuple(qubits_b)


# ---------------------------------------------------------------- commutation

# Diagonal gates: they only add phases, so they commute with each other,
# with the control of a CNOT and with CZ.
DIAGONAL_GATES = {"z", "s", "sdg", "t", "tdg"}


def _single_vs_two(single_name, single_qubit, two_name, two_qubits):
    """
    Commutation of a single-qubit gate with a two-qubit gate that shares
    its qubit.
    """

    if two_name == "cx":
        control, target = two_qubits
        if single_qubit == control and single_name in DIAGONAL_GATES:
            return True   # Z/S/T commute with the CNOT control
        if single_qubit == target and single_name == "x":
            return True   # X commutes with the CNOT target
        return False

    if two_name == "cz":
        return single_name in DIAGONAL_GATES   # CZ is diagonal

    return False   # swap and unknown gates: be safe


def _two_vs_two(name_a, qubits_a, name_b, qubits_b):
    """
    Commutation of two two-qubit gates that share at least one qubit.
    """

    if name_a == name_b and are_inverses(name_a, qubits_a, name_b, qubits_b):
        return True   # identical self-inverse gates commute

    if name_a == "cx" and name_b == "cx":
        control_a, target_a = qubits_a
        control_b, target_b = qubits_b
        # Never commute if one's control is the other's target
        if control_a == target_b or control_b == target_a:
            return False
        return True   # shared control, or shared target

    if name_a == "cz" and name_b == "cz":
        return True   # both diagonal

    if {name_a, name_b} == {"cx", "cz"}:
        cx_qubits = qubits_a if name_a == "cx" else qubits_b
        cz_qubits = qubits_b if name_a == "cx" else qubits_a
        # CZ commutes with a CNOT only if it does not touch the CNOT target
        return cx_qubits[1] not in cz_qubits

    return False   # swap and unknown gates: be safe


def gates_commute(name_a, qubits_a, name_b, qubits_b):
    """
    True only if the two gates can safely swap places without changing what
    the circuit does. When unsure, returns False (never unsafe).
    """

    if not set(qubits_a) & set(qubits_b):
        return True   # gates on different qubits always commute

    if len(qubits_a) == 1 and len(qubits_b) == 1:
        if name_a == name_b:
            return True   # a gate commutes with itself
        return name_a in DIAGONAL_GATES and name_b in DIAGONAL_GATES

    if len(qubits_a) == 1 and len(qubits_b) == 2:
        return _single_vs_two(name_a, qubits_a[0], name_b, tuple(qubits_b))

    if len(qubits_a) == 2 and len(qubits_b) == 1:
        return _single_vs_two(name_b, qubits_b[0], name_a, tuple(qubits_a))

    if len(qubits_a) == 2 and len(qubits_b) == 2:
        return _two_vs_two(name_a, tuple(qubits_a), name_b, tuple(qubits_b))

    return False
