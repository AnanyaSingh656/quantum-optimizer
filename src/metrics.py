def calculate_metrics(circuit):
    """
    Calculate quantum circuit metrics.
    """

    gate_count = len(circuit.data)

    circuit_depth = circuit.depth()

    two_qubit_count = 0
    t_count = 0
    swap_count = 0
    weighted_cost = 0

    for instruction in circuit.data:
        gate_name = instruction.operation.name
        qubit_count = len(instruction.qubits)

        # Count two-qubit gates
        if qubit_count == 2:
            two_qubit_count += 1

        # Count T and T-dagger gates
        if gate_name in ["t", "tdg"]:
            t_count += 1

        # Count SWAP gates
        if gate_name == "swap":
            swap_count += 1

        # Hardware-aware weighted cost
        if gate_name == "swap":
            weighted_cost += 10
        elif qubit_count == 2:
            weighted_cost += 5
        elif gate_name in ["t", "tdg"]:
            weighted_cost += 3
        else:
            weighted_cost += 1

    return {
        "gate_count": gate_count,
        "depth": circuit_depth,
        "two_qubit_count": two_qubit_count,
        "t_count": t_count,
        "swap_count": swap_count,
        "weighted_cost": weighted_cost
    }