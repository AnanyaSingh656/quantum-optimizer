from qiskit import QuantumCircuit


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