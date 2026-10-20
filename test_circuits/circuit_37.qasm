// Circuit 37: Quantum teleportation
// Teleportation of a T-rotated state with deferred-measurement corrections (CX and CZ).
// 3 qubits, 10 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
h q[0];
t q[0];
h q[1];
cx q[1],q[2];
cx q[0],q[1];
h q[0];
cx q[1],q[2];
cz q[0],q[2];
h q[1];
h q[1];
