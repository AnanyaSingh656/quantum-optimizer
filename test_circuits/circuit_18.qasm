// Circuit 18: CNOT ladder, 10 qubits
// CNOT ladder down and back up around a T gate: a parity-phase gadget used in chemistry circuits.
// 10 qubits, 19 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[10];
cx q[0],q[1];
cx q[1],q[2];
cx q[2],q[3];
cx q[3],q[4];
cx q[4],q[5];
cx q[5],q[6];
cx q[6],q[7];
cx q[7],q[8];
cx q[8],q[9];
t q[9];
cx q[8],q[9];
cx q[7],q[8];
cx q[6],q[7];
cx q[5],q[6];
cx q[4],q[5];
cx q[3],q[4];
cx q[2],q[3];
cx q[1],q[2];
cx q[0],q[1];
