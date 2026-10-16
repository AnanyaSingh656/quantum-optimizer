"""
Print every checkpoint circuit, from the original circuit to the final
circuit, with the optimization that produced each one.

Usage (from the project folder):
    python -m src.view_checkpoints                 -> all checkpoint files
    python -m src.view_checkpoints circuit_1.qasm  -> one circuit only
"""

import sys

from qiskit import qasm2

from .main import CHECKPOINT_DIR, CHECKPOINT_START, CHECKPOINT_END
from .benchmarks import _natural_sort_key


def read_checkpoints(checkpoint_path):
    """
    Read a checkpoint file and return a list of
    (checkpoint_number, optimization_type, circuit) in file order.
    """

    checkpoints = []
    current_header = None
    current_lines = []

    with open(checkpoint_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")

            if line.startswith(CHECKPOINT_START):
                # Header looks like:
                # // ===== CHECKPOINT 1 | Inverse-pair cancellation =====
                header = line[len(CHECKPOINT_START):].strip().rstrip("=").strip()
                number, optimization_type = header.split("|", 1)
                current_header = (int(number.strip()), optimization_type.strip())
                current_lines = []

            elif line.startswith(CHECKPOINT_END):
                circuit = qasm2.loads(
                    "\n".join(current_lines),
                    custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS,
                )
                checkpoints.append((*current_header, circuit))
                current_header = None

            elif current_header is not None:
                current_lines.append(line)

    return checkpoints


def print_checkpoints(checkpoint_path):
    """
    Print all checkpoints of one file sequentially.
    """

    print(f"\n########## {checkpoint_path.name} ##########")

    for number, optimization_type, circuit in read_checkpoints(checkpoint_path):
        print(f"\nCheckpoint {number} - Optimization: {optimization_type}")
        print(f"Gates: {len(circuit.data)}")
        print(circuit)


def main():
    if not CHECKPOINT_DIR.exists():
        print("No circuit_outputs folder found. Run 'python -m src.main' first.")
        return

    if len(sys.argv) > 1:
        # Only the checkpoint file of the given circuit name
        checkpoint_files = [CHECKPOINT_DIR / f"checkpoint_{sys.argv[1]}"]
    else:
        # Every checkpoint file in circuit_outputs
        checkpoint_files = sorted(
            CHECKPOINT_DIR.glob("checkpoint_*"),
            key=lambda path: _natural_sort_key(path.name),
        )

    if not checkpoint_files:
        print("No checkpoint files found. Run 'python -m src.main' first.")
        return

    for checkpoint_path in checkpoint_files:
        if not checkpoint_path.exists():
            print(f"Checkpoint file not found: {checkpoint_path}")
            continue
        print_checkpoints(checkpoint_path)


if __name__ == "__main__":
    main()
