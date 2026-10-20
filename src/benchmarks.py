import re
from pathlib import Path

from qiskit import qasm2


# Folder that holds the input circuit files (outside src)
TEST_CIRCUITS_DIR = Path(__file__).resolve().parent.parent / "test_circuits"

# File types that load_circuit() can read
SUPPORTED_EXTENSIONS = [".qasm"]


def _natural_sort_key(name):
    """
    Sort "circuit_2" before "circuit_10" (normal sorting would not).
    """

    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", name)
    ]


def get_all_circuit_names():
    """
    Return the names (with extension) of every circuit file in the
    test_circuits folder, for example:
        ["circuit_1.qasm", "circuit_2.qasm", ...]

    Any number of circuits is supported: just add a new file to the folder.
    """

    if not TEST_CIRCUITS_DIR.exists():
        raise FileNotFoundError(
            f"Circuit folder not found: {TEST_CIRCUITS_DIR}"
        )

    names = [
        path.name
        for path in TEST_CIRCUITS_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    return sorted(names, key=_natural_sort_key)


def load_circuit(circuit_name):
    """
    Create a circuit from a file in the test_circuits folder.

    circuit_name must include the extension, for example:
        "circuit_1.qasm"

    Supported format:
        .qasm  ->  OpenQASM 2.0 circuit description
    """

    circuit_path = TEST_CIRCUITS_DIR / circuit_name

    if not circuit_path.exists():
        raise FileNotFoundError(
            f"Circuit file not found: {circuit_path}"
        )

    extension = circuit_path.suffix.lower()

    if extension == ".qasm":
        # LEGACY_CUSTOM_INSTRUCTIONS adds gates such as swap that are
        # not in the strict OpenQASM 2.0 qelib1.inc library
        circuit = qasm2.load(
            str(circuit_path),
            custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS,
        )
    else:
        raise ValueError(
            f"Unsupported circuit file type '{extension}' "
            f"for {circuit_name}. Use a .qasm file."
        )

    return circuit


def get_all_benchmarks():
    """
    Load every circuit in the test_circuits folder.

    Returns a dictionary {circuit_name: circuit}, e.g.
        {"circuit_1.qasm": <QuantumCircuit>, ...}
    """

    return {
        name: load_circuit(name)
        for name in get_all_circuit_names()
    }
