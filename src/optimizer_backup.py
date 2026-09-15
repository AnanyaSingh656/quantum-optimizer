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