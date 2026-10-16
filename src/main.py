from pathlib import Path

from qiskit import qasm2

from .benchmarks import load_circuit, get_all_circuit_names
from .optimizer import optimize_circuit
from .metrics import calculate_metrics
from .report import print_comparison
from .qiskit_baseline import optimize_with_qiskit
from .verify import check_equivalence


# Circuit files (in the test_circuits folder) to optimize.
# By default every circuit file in the folder is used, so any number of
# circuits works: just add a new .qasm file to test_circuits.
# To run only some circuits, replace this with a list, for example:
#     CIRCUIT_NAMES = ["circuit_1.qasm", "circuit_6.qasm"]
CIRCUIT_NAMES = get_all_circuit_names()

# Folders outside src
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHECKPOINT_DIR = PROJECT_ROOT / "circuit_outputs"
RESULTS_DIR = PROJECT_ROOT / "results"

# Markers used inside a checkpoint file (also read by view_checkpoints.py)
CHECKPOINT_START = "// ===== CHECKPOINT"
CHECKPOINT_END = "// ===== END CHECKPOINT ====="


def save_circuit(circuit, filename):
    """
    Save a circuit diagram into a text file.
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(circuit))


def start_checkpoint_file(circuit_name):
    """
    Create (or overwrite) circuit_outputs/checkpoint_<circuit_name>
    and return its path.
    """

    CHECKPOINT_DIR.mkdir(exist_ok=True)

    checkpoint_path = CHECKPOINT_DIR / f"checkpoint_{circuit_name}"

    with open(checkpoint_path, "w", encoding="utf-8") as file:
        file.write(f"// Checkpoints for {circuit_name}\n\n")

    return checkpoint_path


def add_checkpoint(checkpoint_path, number, optimization_type, circuit):
    """
    Append one circuit to the checkpoint file, labelled with the
    optimization that produced it. The circuit is stored as OpenQASM
    so it can be loaded again later.
    """

    with open(checkpoint_path, "a", encoding="utf-8") as file:
        file.write(
            f"{CHECKPOINT_START} {number} | {optimization_type} =====\n"
        )
        file.write(qasm2.dumps(circuit).strip() + "\n")
        file.write(CHECKPOINT_END + "\n\n")


def optimize_one_circuit(circuit_name, circuit_number):
    """
    Load, optimize, print, store, verify and report one circuit.
    """
    print("==================================================================================================================")
    print(f"=============Circuit {circuit_number}==============")
    print(f"===========File: {circuit_name}==================")
    print("==================================================================================================================")

    # 1) Get the initial circuit from the benchmark loader
    original_circuit = load_circuit(circuit_name)

    print("\nOriginal Circuit:")
    print(original_circuit)

    # Start the checkpoint file with the original circuit
    checkpoint_path = start_checkpoint_file(circuit_name)
    checkpoint_number = 0
    add_checkpoint(
        checkpoint_path, checkpoint_number, "Original circuit", original_circuit
    )

    # 2) Optimize in rounds (see optimize_circuit in optimizer.py).
    #    A checkpoint is saved whenever an optimization changes the circuit.
    def save_change(round_number, optimization_type, new_circuit):
        nonlocal checkpoint_number
        checkpoint_number += 1
        add_checkpoint(
            checkpoint_path,
            checkpoint_number,
            f"Round {round_number} - {optimization_type}",
            new_circuit,
        )

    optimized_circuit, rounds = optimize_circuit(
        original_circuit, on_change=save_change
    )

    print(f"\nOptimization finished after {rounds} round(s) "
          f"({rounds - 1} round(s) with changes + 1 final check)")

    # Final circuit is always stored at the end of the checkpoint file
    checkpoint_number += 1
    add_checkpoint(
        checkpoint_path, checkpoint_number, "Final circuit", optimized_circuit
    )

    # 3) Check that the optimized circuit gives the same result as the original
    check = check_equivalence(original_circuit, optimized_circuit)

    # Qiskit baseline for comparison
    qiskit_circuit = optimize_with_qiskit(original_circuit)

    # Store circuit diagrams (one pair of files per input circuit)
    RESULTS_DIR.mkdir(exist_ok=True)
    stem = Path(circuit_name).stem

    save_circuit(
        original_circuit,
        RESULTS_DIR / f"{stem}_original.txt"
    )

    save_circuit(
        optimized_circuit,
        RESULTS_DIR / f"{stem}_optimized.txt"
    )

    original_metrics = calculate_metrics(original_circuit)
    optimized_metrics = calculate_metrics(optimized_circuit)
    qiskit_metrics = calculate_metrics(qiskit_circuit)

    print("\nOptimized Circuit:")
    print(optimized_circuit)

    print("\nResult check (original vs optimized):")
    print(f"  Same quantum operation (unitary): {check['same_unitary']}")
    print(f"  Same output state from |0...0>:   {check['same_statevector']}")
    print(f"  -> {check['message']}")

    print("\nOriginal Metrics:")
    print(original_metrics)

    print("\nOptimized Metrics:")
    print(optimized_metrics)

    print_comparison(original_metrics, optimized_metrics)

    print("\nQiskit's Optimized Metrics:")
    print(qiskit_metrics)

    print(f"\nCheckpoints saved to: {checkpoint_path}")


def main():
    for circuit_number, circuit_name in enumerate(CIRCUIT_NAMES, start=1):
        optimize_one_circuit(circuit_name, circuit_number)


if __name__ == "__main__":
    main()
