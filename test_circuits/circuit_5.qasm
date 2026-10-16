// Circuit 5: two-qubit gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];

cx q[0],q[1];
cx q[0],q[1];
swap q[1],q[2];
