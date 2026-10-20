from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from src.scheduler import schedule_independent_gates

from src.benchmarks import get_all_benchmarks, get_all_circuit_names
from src.optimizer import optimize_circuit as optimize_in_rounds
from src.verify import check_equivalence
from src.optimizer import (
    cancel_with_commutation_rules,
    merge_single_qubit_gates,
)

def test_scheduler_preserves_statevector():
    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.x(1)
    circuit.cx(0, 1)

    scheduled = schedule_independent_gates(circuit)

    original_state = Statevector.from_instruction(
        circuit
    )

    scheduled_state = Statevector.from_instruction(
        scheduled
    )

    assert original_state.equiv(
        scheduled_state
    )


def optimize_circuit(circuit):
    """
    Apply our complete optimization pipeline (round-wise, same as main.py).
    """
    optimized_circuit, rounds = optimize_in_rounds(circuit)

    return optimized_circuit


def test_basic_circuit_creation():
    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.cx(0, 1)

    assert circuit.num_qubits == 2
    assert circuit.size() == 2


def test_h_gate_cancellation():
    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.h(0)

    optimized = optimize_circuit(circuit)

    assert optimized.size() == 0


def test_x_gate_cancellation():
    circuit = QuantumCircuit(1)

    circuit.x(0)
    circuit.x(0)

    optimized = optimize_circuit(circuit)

    assert optimized.size() == 0


def test_inverse_gate_cancellation():
    circuit = QuantumCircuit(1)

    circuit.t(0)
    circuit.tdg(0)

    optimized = optimize_circuit(circuit)

    assert optimized.size() == 0


def test_commutation_cancellation():
    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.x(1)
    circuit.h(0)

    optimized = optimize_circuit(circuit)

    assert optimized.size() == 1
    assert optimized.data[0].operation.name == "x"


def test_statevector_preservation():
    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.x(1)
    circuit.h(0)

    optimized = optimize_circuit(circuit)

    original_state = Statevector.from_instruction(circuit)
    optimized_state = Statevector.from_instruction(optimized)

    assert original_state.equiv(optimized_state)


def test_all_benchmarks_preserve_statevector():
    benchmarks = get_all_benchmarks()

    for name, original_circuit in benchmarks.items():
        optimized_circuit = optimize_circuit(
            original_circuit
        )

        original_state = Statevector.from_instruction(
            original_circuit
        )

        optimized_state = Statevector.from_instruction(
            optimized_circuit
        )

        assert original_state.equiv(
            optimized_state
        ), f"Statevector changed for benchmark: {name}"


def test_circuits_are_loaded_from_folder():
    names = get_all_circuit_names()

    assert len(names) > 0
    assert all(name.endswith(".qasm") for name in names)


def test_round_wise_optimization():
    # Round 1: merging turns H X H into Z.
    # Round 2: that Z cancels with the other Z through the CNOT control.
    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.x(0)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.z(0)

    optimized, rounds = optimize_in_rounds(circuit)

    assert optimized.size() == 1
    assert optimized.data[0].operation.name == "cx"
    assert rounds == 3  # 2 rounds with changes + 1 final check
    assert check_equivalence(circuit, optimized)["equivalent"]


def test_all_benchmarks_pass_result_check():
    for name, original_circuit in get_all_benchmarks().items():
        optimized_circuit = optimize_circuit(original_circuit)

        check = check_equivalence(original_circuit, optimized_circuit)

        assert check["equivalent"], f"Result changed for benchmark: {name}"


def test_merge_h_x_h_into_z():
    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.x(0)
    circuit.h(0)

    merged = merge_single_qubit_gates(circuit)

    assert merged.size() == 1
    assert merged.data[0].operation.name == "z"
    assert check_equivalence(circuit, merged)["equivalent"]


def test_merge_t_t_into_s():
    circuit = QuantumCircuit(1)

    circuit.t(0)
    circuit.t(0)

    merged = merge_single_qubit_gates(circuit)

    assert merged.size() == 1
    assert merged.data[0].operation.name == "s"


def test_merge_to_identity_removes_gates():
    circuit = QuantumCircuit(1)

    circuit.x(0)
    circuit.y(0)
    circuit.z(0)

    assert merge_single_qubit_gates(circuit).size() == 0


def test_cancel_through_cnot_control():
    # T on the control commutes with the CNOT, so T and T† cancel
    circuit = QuantumCircuit(2)

    circuit.t(0)
    circuit.cx(0, 1)
    circuit.tdg(0)

    optimized = cancel_with_commutation_rules(circuit)

    assert optimized.size() == 1
    assert optimized.data[0].operation.name == "cx"
    assert check_equivalence(circuit, optimized)["equivalent"]


def test_no_cancel_through_cnot_target():
    # T on the TARGET does NOT commute with the CNOT: must stay unchanged
    circuit = QuantumCircuit(2)

    circuit.t(1)
    circuit.cx(0, 1)
    circuit.tdg(1)

    optimized = cancel_with_commutation_rules(circuit)

    assert optimized.size() == 3
