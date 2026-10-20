// Circuit 1: mixed benchmark (same as create_benchmark_circuit)
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];

// Adjacent cancellation
h q[0];
h q[0];

// Commutation cancellation
x q[1];
h q[0];
h q[0];

// Non-cancellable pattern
h q[2];
x q[2];
h q[2];

// Two-qubit gates
cx q[0],q[1];
cx q[1],q[2];

// T and T-dagger cancellation
t q[0];
tdg q[0];

// SWAP gate
swap q[1],q[2];
