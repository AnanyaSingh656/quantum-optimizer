# Random circuit generator demo

Generates one random circuit, runs it through our optimizer and Qiskit, and shows the metrics, tables, circuit drawings and charts.

## How to run

1. Install the packages with `python -m pip install -r requirements.txt`.
2. Open the project root folder in VS Code, then open `single_random_circuit_demo.ipynb`.
3. Click **Select Kernel** (top right) and pick the Python you installed the packages into.
4. Set the parameters in the parameters cell.
5. Click **Run All**.

Charts and circuit drawings are also saved in `results/plots/`.

## Parameters

| Parameter | Meaning |
|---|---|
| `QUBITS` | Number of qubits. Keep it at 10 or below so equivalence can be checked. |
| `GATES` | Target number of gates. The actual count can be a few higher. |
| `REDUNDANCY` | Probability (0 to 1) that each step inserts a removable gate pattern instead of a single random gate. 0 gives a fully random circuit; higher values give the optimizer more to remove. |
| `SEED` | Fixes the random choices. The same seed and parameters always give the same circuit; a different seed gives a different one. |