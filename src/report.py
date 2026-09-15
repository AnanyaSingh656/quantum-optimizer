def print_comparison(original_metrics, optimized_metrics):
    """
    Display the improvement after optimization.
    """

    original_gate_count = original_metrics["gate_count"]
    optimized_gate_count = optimized_metrics["gate_count"]

    original_depth = original_metrics["depth"]
    optimized_depth = optimized_metrics["depth"]

    original_two_qubit = original_metrics["two_qubit_count"]
    optimized_two_qubit = optimized_metrics["two_qubit_count"]

    original_t_count = original_metrics["t_count"]
    optimized_t_count = optimized_metrics["t_count"]

    original_swap_count = original_metrics["swap_count"]
    optimized_swap_count = optimized_metrics["swap_count"]

    original_weighted_cost = original_metrics["weighted_cost"]
    optimized_weighted_cost = optimized_metrics["weighted_cost"]

    if original_gate_count > 0:
        gate_reduction = (
            (original_gate_count - optimized_gate_count)
            / original_gate_count
        ) * 100
    else:
        gate_reduction = 0

    if original_depth > 0:
        depth_reduction = (
            (original_depth - optimized_depth)
            / original_depth
        ) * 100
    else:
        depth_reduction = 0

    if original_weighted_cost > 0:
        weighted_cost_reduction = (
            (original_weighted_cost - optimized_weighted_cost)
            / original_weighted_cost
        ) * 100
    else:
        weighted_cost_reduction = 0

    print("\n========== Optimization Report ==========")

    print(f"Gate count: {original_gate_count} -> {optimized_gate_count}")
    print(f"Gate reduction: {gate_reduction:.2f}%")

    print(f"Depth: {original_depth} -> {optimized_depth}")
    print(f"Depth reduction: {depth_reduction:.2f}%")

    print(
        "Two-qubit gates: "
        f"{original_two_qubit} -> {optimized_two_qubit}"
    )

    print(f"T-count: {original_t_count} -> {optimized_t_count}")

    print(f"SWAP count: {original_swap_count} -> {optimized_swap_count}")

    print(
        f"Weighted cost reduction: "
        f"{weighted_cost_reduction:.2f}%"
    )

    print("=========================================")