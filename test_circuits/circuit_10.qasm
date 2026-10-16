// Circuit 10: Toffoli gate
// One Toffoli (CCX) gate in its standard Clifford+T form: 7 T gates, 6 CNOTs.
// 3 qubits, 15 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
h q[2];
cx q[1],q[2];
tdg q[2];
cx q[0],q[2];
t q[2];
cx q[1],q[2];
tdg q[2];
cx q[0],q[2];
t q[1];
t q[2];
h q[2];
cx q[0],q[1];
t q[0];
tdg q[1];
cx q[0],q[1];
