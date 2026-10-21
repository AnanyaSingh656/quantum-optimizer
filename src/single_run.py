"""
Single random-circuit experiment:

    generate -> optimize (ours + Qiskit) -> verify -> metrics -> report -> graphs

Used by the notebook (single_circuit_demo.ipynb) and runnable from a terminal
at the project root:

    python -m src.single_run --qubits 5 --gates 80 --redundancy 0.4 --seed 7
    python -m src.single_run --seed 7 --show        # also open the chart window
"""

import argparse
import time
from pathlib import Path

import pandas as pd

from .generator import generate_circuit
from .metrics import calculate_metrics
from .optimizer import optimize_circuit
from .qiskit_baseline import optimize_with_qiskit
from .verify import check_equivalence

METHODS = ["Original", "Ours", "Qiskit"]
COLORS = {"Original": "#9aa0a6", "Ours": "#1a73e8", "Qiskit": "#e8710a"}

# (metrics key, readable name) in the order they are tabulated and plotted
METRIC_KEYS = [
    ("gate_count", "Gate count"),
    ("depth", "Circuit depth"),
    ("weighted_cost", "Weighted cost"),
    ("two_qubit_count", "Two-qubit gates"),
    ("t_count", "T-count"),
    ("swap_count", "SWAP count"),
]


def reduction_percent(original_value, new_value):
    """How much smaller new_value is than original_value, in percent."""
    if original_value == 0:
        return 0.0
    return (original_value - new_value) / original_value * 100


def run_single(qubits=4, gates=60, redundancy=0.3, seed=0):
    """
    Generate one random circuit, run both optimizers on it, verify and measure.

    Returns a dict with the circuits, metrics, timings, equivalence flags and
    two DataFrames: `table` (absolute values) and `reduction` (% vs original).
    """
    if qubits < 1:
        raise ValueError("qubits must be at least 1")
    if gates < 1:
        raise ValueError("gates must be at least 1")
    if not 0 <= redundancy <= 1:
        raise ValueError("redundancy must be between 0 and 1")

    original = generate_circuit(qubits, gates, redundancy, seed)

    start = time.perf_counter()
    ours, rounds = optimize_circuit(original)
    ours_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    qiskit_circuit = optimize_with_qiskit(original)
    qiskit_ms = (time.perf_counter() - start) * 1000

    # None means "not checked" (circuit too large for the unitary check)
    ours_equivalent = check_equivalence(original, ours)
    qiskit_equivalent = check_equivalence(original, qiskit_circuit)

    circuits = {"Original": original, "Ours": ours, "Qiskit": qiskit_circuit}
    metrics = {name: calculate_metrics(circ) for name, circ in circuits.items()}
    times_ms = {"Original": None, "Ours": ours_ms, "Qiskit": qiskit_ms}

    table = pd.DataFrame(
        {m: {label: metrics[m][key] for key, label in METRIC_KEYS} for m in METHODS}
    )
    table.loc["Compile time (ms)"] = [times_ms[m] for m in METHODS]

    reduction = pd.DataFrame(
        {
            m: {
                label: reduction_percent(metrics["Original"][key], metrics[m][key])
                for key, label in METRIC_KEYS
            }
            for m in ["Ours", "Qiskit"]
        }
    )

    return {
        "params": {
            "qubits": qubits,
            "gates": gates,
            "redundancy": redundancy,
            "seed": seed,
        },
        "circuits": circuits,
        "metrics": metrics,
        "times_ms": times_ms,
        "rounds": rounds,
        "equivalent": {"Ours": ours_equivalent, "Qiskit": qiskit_equivalent},
        "table": table,
        "reduction": reduction,
    }


def _equivalence_text(value):
    if value is None:
        return "not checked (too many qubits)"
    return "yes" if value else "NO - results are not trustworthy"


def print_report(result, max_diagram_gates=40):
    """Print parameters, verification status, tables and (small) circuit diagrams."""
    p = result["params"]
    original = result["circuits"]["Original"]

    print(
        f"Circuit: {p['qubits']} qubits, target {p['gates']} gates "
        f"(actual {original.size()}), redundancy {p['redundancy']}, seed {p['seed']}"
    )
    print(f"Optimizer rounds: {result['rounds']}")
    print(f"Equivalent to original - ours: {_equivalence_text(result['equivalent']['Ours'])}")
    print(f"Equivalent to original - Qiskit: {_equivalence_text(result['equivalent']['Qiskit'])}")

    print("\nMetrics")
    print(result["table"].round(2).to_string(na_rep="-"))
    print("\nReduction vs original (%)")
    print(result["reduction"].round(1).to_string())

    for name in METHODS:
        circ = result["circuits"][name]
        if circ.size() <= max_diagram_gates:
            print(f"\n{name} ({circ.size()} gates)")
            print(circ.draw("text", fold=120))
        else:
            print(f"\n{name}: {circ.size()} gates, diagram skipped (limit {max_diagram_gates})")


def draw_circuits(result, max_gates=80, fold=40, save_dir=None, show=True):
    """
    Draw Original / Ours / Qiskit circuits graphically (Qiskit's "mpl" drawer).

    Circuits with more than `max_gates` gates are skipped, since they become
    unreadable. `fold` wraps long circuits onto several rows.
    Needs the `pylatexenc` package (listed in requirements.txt).
    """
    import matplotlib.pyplot as plt

    figs = {}
    for name in METHODS:
        circ = result["circuits"][name]
        if circ.size() > max_gates:
            print(f"{name}: {circ.size()} gates, drawing skipped (limit {max_gates})")
            continue
        fig = circ.draw("mpl", fold=fold)
        fig.suptitle(f"{name} ({circ.size()} gates)", fontsize=12)
        if save_dir:
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            fig.savefig(Path(save_dir) / f"circuit_{name.lower()}.png",
                        dpi=150, bbox_inches="tight")
        figs[name] = fig
    if show:
        plt.show()
    return figs


def plot_single(result, save_path=None, show=True):
    """Bar charts of every metric for Original / Ours / Qiskit, plus compile time."""
    import matplotlib.pyplot as plt

    metrics = result["metrics"]
    p = result["params"]

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    panels = METRIC_KEYS[:5]  # swap count is in the table only (usually 0)

    for ax, (key, label) in zip(axes.flat, panels):
        values = [metrics[m][key] for m in METHODS]
        bars = ax.bar(METHODS, values, color=[COLORS[m] for m in METHODS])
        ax.bar_label(bars, padding=2)
        ax.set_title(label)
        ax.margins(y=0.15)

    ax = axes.flat[5]
    timed = ["Ours", "Qiskit"]
    values = [result["times_ms"][m] for m in timed]
    bars = ax.bar(timed, values, color=[COLORS[m] for m in timed])
    ax.bar_label(bars, fmt="%.1f", padding=2)
    ax.set_title("Compile time (ms)")
    ax.margins(y=0.15)

    for ax in axes.flat:
        ax.spines[["top", "right"]].set_visible(False)

    ok = result["equivalent"]
    status = "verified" if ok["Ours"] else ("not checked" if ok["Ours"] is None else "NOT EQUIVALENT")
    fig.suptitle(
        f"{p['qubits']} qubits, {result['circuits']['Original'].size()} gates, "
        f"redundancy {p['redundancy']}, seed {p['seed']}  |  ours: {status}",
        fontsize=12,
    )
    fig.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--qubits", type=int, default=4)
    parser.add_argument("--gates", type=int, default=60)
    parser.add_argument("--redundancy", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out-dir", default="results/plots")
    parser.add_argument("--show", action="store_true", help="open the chart window")
    args = parser.parse_args()

    if not args.show:
        import matplotlib
        matplotlib.use("Agg")

    result = run_single(args.qubits, args.gates, args.redundancy, args.seed)
    print_report(result)

    name = f"single_q{args.qubits}_g{args.gates}_r{args.redundancy}_s{args.seed}.png"
    path = Path(args.out_dir) / name
    plot_single(result, save_path=path, show=args.show)
    print(f"\nChart saved to {path}")


if __name__ == "__main__":
    main()
