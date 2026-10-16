// Circuit 14: Toffoli with redundancy
// A Toffoli surrounded by leftover gate pairs (H H, T T-dagger, S S-dagger) from earlier compilation.
// 3 qubits, 23 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
h q[2];
h q[2];
t q[0];
tdg q[0];
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
s q[1];
sdg q[1];
h q[2];
h q[2];
