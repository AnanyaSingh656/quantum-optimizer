from qiskit import QuantumCircuit
from qiskit.circuit.library import (
    HGate, XGate, YGate, ZGate, SGate, SdgGate, TGate, TdgGate,
)

from .gate_rules import (
    MERGEABLE_GATES,
    INVERSE_OF,
    are_inverses,
    gates_commute,
    matrix_to_gate,
    product_of_gates,
)


def cancel_adjacent_gates(circuit):
    """
    Remove adjacent identical gates acting
    on the same qubits.

    Examples:
        H H   -> removed
        X X   -> removed
        CX CX -> removed
    """

    optimized_circuit = QuantumCircuit(circuit.num_qubits)

    index = 0

    while index < len(circuit.data):

        current_instruction = circuit.data[index]

        # If there is a next gate, compare both gates
        if index + 1 < len(circuit.data):

            next_instruction = circuit.data[index + 1]

            current_gate = current_instruction.operation
            next_gate = next_instruction.operation

            current_qubits = current_instruction.qubits
            next_qubits = next_instruction.qubits

            # Check whether both gates are identical
            if (
                current_gate.name == next_gate.name
                and current_qubits == next_qubits
                and current_gate.name in ["h", "x", "cx"]
            ):
                # Skip both gates because they cancel
                index += 2
                continue

        # Keep the current gate if it cannot be cancelled
        optimized_circuit.append(
            current_instruction.operation,
            current_instruction.qubits,
            current_instruction.clbits
        )

        index += 1

    return optimized_circuit

def cancel_with_commutation(circuit):
    """
    Cancel identical gates separated by gates
    acting on different qubits.

    Example:
        H(0) -> X(1) -> H(0)

    becomes:
        X(1)
    """

    instructions = list(circuit.data)

    removed = set()

    for i in range(len(instructions)):

        if i in removed:
            continue

        first_instruction = instructions[i]
        first_gate = first_instruction.operation

        # Only handle H and X gates for now
        if first_gate.name not in ["h", "x"]:
            continue

        for j in range(i + 1, len(instructions)):

            if j in removed:
                continue

            second_instruction = instructions[j]
            second_gate = second_instruction.operation

            # Stop if the same gate is not found
            if (
                first_gate.name == second_gate.name
                and first_instruction.qubits == second_instruction.qubits
            ):

                # Check all gates between the two matching gates
                can_commute = True

                for k in range(i + 1, j):

                    if k in removed:
                        continue

                    middle_instruction = instructions[k]

                    # If the middle gate uses the same qubit,
                    # we cannot safely move through it
                    if set(first_instruction.qubits) & set(
                        middle_instruction.qubits
                    ):
                        can_commute = False
                        break

                if can_commute:
                    removed.add(i)
                    removed.add(j)

                break

    optimized_circuit = QuantumCircuit(circuit.num_qubits)

    for index, instruction in enumerate(instructions):

        if index not in removed:
            optimized_circuit.append(
                instruction.operation,
                instruction.qubits,
                instruction.clbits
            )

    return optimized_circuit

def cancel_inverse_gates(circuit):
    """
    Remove adjacent inverse quantum gates.

    Examples:
        H  H     -> removed
        X  X     -> removed
        T  Tdg   -> removed
        Tdg T    -> removed
        CX CX    -> removed
        SWAP SWAP -> removed
    """

    self_inverse_gates = {
        "h",
        "x",
        "y",
        "z",
        "cx",
        "cz",
        "swap"
    }

    inverse_gate_pairs = {
        ("t", "tdg"),
        ("tdg", "t"),
        ("s", "sdg"),
        ("sdg", "s")
    }

    optimized_circuit = QuantumCircuit(circuit.num_qubits)

    index = 0

    while index < len(circuit.data):

        current_instruction = circuit.data[index]

        if index + 1 < len(circuit.data):

            next_instruction = circuit.data[index + 1]

            current_name = current_instruction.operation.name
            next_name = next_instruction.operation.name

            same_qubits = (
                current_instruction.qubits
                == next_instruction.qubits
            )

            is_self_inverse_pair = (
                current_name == next_name
                and current_name in self_inverse_gates
            )

            is_inverse_pair = (
                current_name,
                next_name
            ) in inverse_gate_pairs

            if same_qubits and (
                is_self_inverse_pair or is_inverse_pair
            ):
                # Skip both gates because they cancel
                index += 2
                continue

        optimized_circuit.append(
            current_instruction.operation,
            current_instruction.qubits,
            current_instruction.clbits
        )

        index += 1

    return optimized_circuit


def _qubit_indices(circuit, instruction):
    """Qubit numbers (0, 1, ...) that an instruction acts on."""

    return tuple(circuit.find_bit(qubit).index for qubit in instruction.qubits)


def cancel_with_commutation_rules(circuit):
    """
    Remove pairs of gates that cancel, even when other gates sit between
    them, as long as the first gate can be moved past every gate in between.

    Improvements over cancel_with_commutation():
      - works for every cancelling pair: H H, X X, Y Y, Z Z, T T†, S S†,
        CX CX, CZ CZ, SWAP SWAP (not only H and X)
      - uses the commutation rules in gate_rules.py, so it can look past
        gates on the SAME qubit when they commute, e.g.

            T(0)  CX(0,1)  T†(0)   ->   CX(0,1)
            (T commutes with the control of the CNOT)
    """

    instructions = list(circuit.data)
    qubits = [_qubit_indices(circuit, inst) for inst in instructions]
    removed = set()

    for i in range(len(instructions)):

        if i in removed:
            continue

        name_i = instructions[i].operation.name

        if name_i not in INVERSE_OF or instructions[i].clbits:
            continue

        # Walk forward, moving gate i past every gate it commutes with,
        # until we find the gate that undoes it or hit a blocking gate.
        for j in range(i + 1, len(instructions)):

            if j in removed:
                continue

            name_j = instructions[j].operation.name

            if are_inverses(name_i, qubits[i], name_j, qubits[j]):
                removed.add(i)
                removed.add(j)
                break

            if not gates_commute(name_i, qubits[i], name_j, qubits[j]):
                break   # gate i cannot move past gate j

    optimized_circuit = circuit.copy_empty_like()

    for index, instruction in enumerate(instructions):
        if index not in removed:
            optimized_circuit.append(
                instruction.operation,
                instruction.qubits,
                instruction.clbits
            )

    return optimized_circuit


_GATE_OBJECTS = {
    "h": HGate, "x": XGate, "y": YGate, "z": ZGate,
    "s": SGate, "sdg": SdgGate, "t": TGate, "tdg": TdgGate,
}


def _merge_run(names):
    """
    Merge a run of single-qubit gate names on one qubit.

    Greedy, left to right: from each position take the LONGEST stretch
    (at least 2 gates) whose product equals one gate or the identity.

    Returns a list of (start, end, result) with result = "id" (remove the
    stretch) or a gate name (replace the stretch with that one gate).
    """

    merges = []
    start = 0

    while start < len(names):
        best = None

        for end in range(len(names) - 1, start, -1):
            result = matrix_to_gate(product_of_gates(names[start:end + 1]))
            if result is not None:
                best = (start, end, result)
                break

        if best is None:
            start += 1
        else:
            merges.append(best)
            start = best[1] + 1

    return merges


def merge_single_qubit_gates(circuit):
    """
    Replace runs of back-to-back single-qubit gates on the same qubit with
    ONE equivalent gate, or remove them if they multiply to nothing:

        H X H  ->  Z        T T  ->  S        S S  ->  Z
        T T T T -> Z        H Z H -> X        X Y Z -> (removed)

    Only gates from our own gate set (H, X, Y, Z, S, S†, T, T†) are ever
    produced, and the circuit stays exactly equivalent (no qubit relabeling).
    """

    instructions = list(circuit.data)

    # result[index] = None (keep), "remove", or a gate object to put there
    result = [None] * len(instructions)

    # Current run of mergeable gates on each qubit: list of instruction indices
    runs = {}

    def flush(qubit):
        run = runs.pop(qubit, [])
        if len(run) < 2:
            return
        names = [instructions[k].operation.name for k in run]
        for start, end, merged in _merge_run(names):
            for k in run[start:end + 1]:
                result[k] = "remove"
            if merged != "id":
                # Put the single replacement gate where the stretch started
                result[run[start]] = _GATE_OBJECTS[merged]()

    for index, instruction in enumerate(instructions):
        qubits = _qubit_indices(circuit, instruction)
        name = instruction.operation.name

        if (
            len(qubits) == 1
            and name in MERGEABLE_GATES
            and not instruction.clbits
        ):
            runs.setdefault(qubits[0], []).append(index)
        else:
            # Any other gate on these qubits ends their runs
            for qubit in qubits:
                flush(qubit)

    for qubit in list(runs):
        flush(qubit)

    optimized_circuit = circuit.copy_empty_like()

    for index, instruction in enumerate(instructions):
        action = result[index]
        if action is None:
            optimized_circuit.append(
                instruction.operation, instruction.qubits, instruction.clbits
            )
        elif action != "remove":
            optimized_circuit.append(action, instruction.qubits)

    return optimized_circuit


# Optimizations applied in every round, in this order
# (the original cancel_with_commutation is kept above for comparison,
#  but cancel_with_commutation_rules replaces it in the pipeline)
#
# Order matters for the checkpoints:
#   1. Inverse-pair cancellation removes pairs that are directly next to
#      each other (H H, T T†, CX CX, ...).
#   2. Commutation-rules cancellation then removes the pairs that are
#      separated by other gates. It can also remove adjacent pairs, so if
#      it ran first, inverse-pair cancellation would never get anything to
#      do and would never appear in the checkpoints.
#   3. Single-qubit gate merging combines what is left (H X H -> Z, ...).
OPTIMIZATIONS = [
    ("Inverse-pair cancellation", cancel_inverse_gates),
    ("Commutation-rules cancellation", cancel_with_commutation_rules),
    ("Single-qubit gate merging", merge_single_qubit_gates),
]


def optimize_circuit(circuit, on_change=None):
    """
    Full optimization pipeline, run in rounds.

    One cancellation can bring two other gates next to each other, so the
    whole list of OPTIMIZATIONS is repeated until a full round removes no
    more gates.

    on_change (optional) is called as
        on_change(round_number, optimization_type, new_circuit)
    every time an optimization changes the circuit (used by main.py to
    save checkpoints).

    Returns (optimized_circuit, number_of_rounds).
    """

    current_circuit = circuit
    round_number = 0

    while True:
        round_number += 1
        gates_before_round = len(current_circuit.data)

        for optimization_type, optimization in OPTIMIZATIONS:
            new_circuit = optimization(current_circuit)

            # The optimizations only remove gates, so a different gate
            # count means the circuit changed.
            if len(new_circuit.data) != len(current_circuit.data):
                if on_change is not None:
                    on_change(round_number, optimization_type, new_circuit)

            current_circuit = new_circuit

        # A full round removed nothing: no further round can help.
        if len(current_circuit.data) == gates_before_round:
            break

    return current_circuit, round_number
