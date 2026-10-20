// Circuit 34: Repetition-code syndrome cycles
// Three syndrome-extraction cycles of a 3-qubit repetition code (data 0,2,4; ancillas 1,3).
// 5 qubits, 24 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
cx q[0],q[1];
cx q[2],q[1];
cx q[2],q[3];
cx q[4],q[3];
h q[1];
h q[3];
h q[1];
h q[3];
cx q[0],q[1];
cx q[2],q[1];
cx q[2],q[3];
cx q[4],q[3];
h q[1];
h q[3];
h q[1];
h q[3];
cx q[0],q[1];
cx q[2],q[1];
cx q[2],q[3];
cx q[4],q[3];
h q[1];
h q[3];
h q[1];
h q[3];
