from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from src.scheduler import schedule_independent_gates

from src.benchmarks import get_all_benchmarks
from src.optimizer import (
    cancel_with_commutation,
    cancel_inverse_gates,
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
    Apply our complete optimization pipeline.
    """
    commutation_circuit = cancel_with_commutation(circuit)

    optimized_circuit = cancel_inverse_gates(
        commutation_circuit
    )

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