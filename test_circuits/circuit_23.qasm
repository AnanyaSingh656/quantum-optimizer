// Circuit 23: Hidden shift, 6 qubits
// Hidden-shift algorithm with bent functions made of CZ gates and a shift of X gates.
// 6 qubits, 28 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[6];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
x q[1];
x q[4];
cz q[0],q[1];
cz q[2],q[3];
cz q[4],q[5];
x q[1];
x q[4];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
cz q[0],q[1];
cz q[2],q[3];
cz q[4],q[5];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
