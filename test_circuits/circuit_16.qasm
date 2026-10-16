// Circuit 16: GHZ mirror
// Prepares a 6-qubit GHZ state and then un-prepares it. The whole circuit equals doing nothing.
// 6 qubits, 12 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[6];
h q[0];
cx q[0],q[1];
cx q[1],q[2];
cx q[2],q[3];
cx q[3],q[4];
cx q[4],q[5];
cx q[4],q[5];
cx q[3],q[4];
cx q[2],q[3];
cx q[1],q[2];
cx q[0],q[1];
h q[0];
