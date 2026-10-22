"""
Random redundant circuit generator.

Only uses the gates the optimizer understands:
    1-qubit: h x y z s sdg t tdg
    2-qubit: cx cz swap

Each circuit is a stream of random gates, and with probability `redundancy`
each step instead inserts a redundancy pattern the optimizer should be able
to remove or shrink:

    adjacent   : g g^-1                       (inverse-pair cancellation)
    gap        : g ...commuting gates... g^-1 (commutation-rules cancellation)
    merge      : H X H, T T, S S, T T T T     (single-qubit merging)

Usage (from the project root):
    python -m src.generator --count 20 --seed 1
    python -m src.generator --count 10 --qubits 4 8 --gates 40 200 \
        --redundancy 0.4 --out test_circuits_random

Same seed + same arguments -> identical circuits (reproducible).
Writes circuit_XX.qasm files plus manifest.json (parameters per circuit).
"""

import argparse
import json
import random
from pathlib import Path

from qiskit import QuantumCircuit, qasm2

ONE_QUBIT = ["h", "x", "y", "z", "s", "sdg", "t", "tdg"]
TWO_QUBIT = ["cx", "cz", "swap"]
DIAGONAL = ["z", "s", "sdg", "t", "tdg"]

INVERSE = {
    "h": "h", "x": "x", "y": "y", "z": "z",
    "s": "sdg", "sdg": "s", "t": "tdg", "tdg": "t",
    "cx": "cx", "cz": "cz", "swap": "swap",
}

# Single-qubit runs that multiply to one gate or to nothing
MERGE_RUNS = [
    ["h", "x", "h"], ["h", "z", "h"], ["t", "t"], ["s", "s"],
    ["t", "t", "t", "t"], ["x", "y", "z"], ["s", "z", "sdg"],
]


def _apply(qc, name, qubits):
    getattr(qc, name)(*qubits)


def _random_gate(qc, rng):
    n = qc.num_qubits
    if n > 1 and rng.random() < 0.3:
        name = rng.choice(TWO_QUBIT)
        _apply(qc, name, rng.sample(range(n), 2))
    else:
        _apply(qc, rng.choice(ONE_QUBIT), [rng.randrange(n)])


def _adjacent(qc, rng):
    n = qc.num_qubits
    if n > 1 and rng.random() < 0.4:
        name = rng.choice(TWO_QUBIT)
        qubits = rng.sample(range(n), 2)
    else:
        name = rng.choice(ONE_QUBIT)
        qubits = [rng.randrange(n)]
    _apply(qc, name, qubits)
    _apply(qc, INVERSE[name], qubits)


def _gap(qc, rng):
    """A gate, then gates it commutes with, then its inverse."""
    n = qc.num_qubits
    kind = rng.choice(["other_qubits", "diag_on_control", "x_on_target", "diag_on_cz"])

    if n < 2:
        return _adjacent(qc, rng)

    q, r = rng.sample(range(n), 2)

    if kind == "other_qubits":
        name = rng.choice(ONE_QUBIT)
        _apply(qc, name, [q])
        others = [x for x in range(n) if x != q]
        for _ in range(rng.randint(1, 3)):
            _random_on(qc, rng, others)
        _apply(qc, INVERSE[name], [q])
    elif kind == "diag_on_control":
        d = rng.choice(DIAGONAL)
        _apply(qc, d, [q])
        qc.cx(q, r)
        _apply(qc, INVERSE[d], [q])
    elif kind == "x_on_target":
        qc.x(r)
        qc.cx(q, r)
        qc.x(r)
    else:  # diag_on_cz
        d = rng.choice(DIAGONAL)
        _apply(qc, d, [q])
        qc.cz(q, r)
        _apply(qc, INVERSE[d], [q])


def _random_on(qc, rng, allowed):
    """Random 1- or 2-qubit gate using only qubits in `allowed`."""
    if len(allowed) > 1 and rng.random() < 0.3:
        _apply(qc, rng.choice(TWO_QUBIT), rng.sample(allowed, 2))
    else:
        _apply(qc, rng.choice(ONE_QUBIT), [rng.choice(allowed)])


def _merge(qc, rng):
    q = rng.randrange(qc.num_qubits)
    for name in rng.choice(MERGE_RUNS):
        _apply(qc, name, [q])


PATTERNS = [_adjacent, _gap, _merge]


def generate_circuit(num_qubits, num_gates, redundancy, seed):
    """
    Build one circuit. Gate count lands at num_gates or a few above it
    (a redundancy pattern is never cut in half).
    """
    rng = random.Random(seed)
    qc = QuantumCircuit(num_qubits)

    while qc.size() < num_gates:
        if rng.random() < redundancy:
            rng.choice(PATTERNS)(qc, rng)
        else:
            _random_gate(qc, rng)

    return qc


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--count", type=int, default=10, help="number of circuits")
    p.add_argument("--qubits", type=int, nargs=2, default=[2, 8], metavar=("MIN", "MAX"))
    p.add_argument("--gates", type=int, nargs=2, default=[20, 150], metavar=("MIN", "MAX"))
    p.add_argument("--redundancy", type=float, default=0.3,
                   help="chance (0-1) that a step inserts a redundancy pattern")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", default="test_circuits_random")
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    master = random.Random(args.seed)
    manifest = []

    for i in range(1, args.count + 1):
        n = master.randint(*args.qubits)
        g = master.randint(*args.gates)
        circuit_seed = master.randrange(2**31)
        qc = generate_circuit(n, g, args.redundancy, circuit_seed)

        name = f"circuit_{i}.qasm"
        (out / name).write_text(qasm2.dumps(qc))
        manifest.append({
            "file": name, "qubits": n, "target_gates": g,
            "actual_gates": qc.size(), "redundancy": args.redundancy,
            "circuit_seed": circuit_seed, "master_seed": args.seed,
        })

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {args.count} circuits + manifest.json to {out}/")


if __name__ == "__main__":
    main()
