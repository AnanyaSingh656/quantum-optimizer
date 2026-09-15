from qiskit import QuantumCircuit


def schedule_independent_gates(circuit):
    """
    Schedule gates into layers.

    Gates using different qubits can be placed in the same layer.
    Gates using the same qubit must remain in their original order.
    """

    layers = []

    for instruction in circuit.data:
        operation = instruction.operation
        qubits = instruction.qubits
        clbits = instruction.clbits

        current_qubits = {
            circuit.find_bit(qubit).index
            for qubit in qubits
        }

        placed = False

        # Try to place the gate in the earliest compatible layer
        for layer in layers:

            layer_qubits = set()

            for previous_operation, previous_qubits, previous_clbits in layer:
                for qubit in previous_qubits:
                    layer_qubits.add(
                        circuit.find_bit(qubit).index
                    )

            # No shared qubits means the gates can run together
            if not current_qubits.intersection(layer_qubits):
                layer.append(
                    (operation, qubits, clbits)
                )
                placed = True
                break

        # If no compatible layer exists, create a new layer
        if not placed:
            layers.append(
                [(operation, qubits, clbits)]
            )

    # Rebuild the scheduled circuit
    scheduled_circuit = QuantumCircuit(
        circuit.num_qubits,
        circuit.num_clbits
    )

    for layer in layers:
        for operation, qubits, clbits in layer:
            scheduled_circuit.append(
                operation,
                qubits,
                clbits
            )

    return scheduled_circuit