// Circuit 4: inverse gate pairs
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];

t q[0];
tdg q[0];
s q[1];
sdg q[1];
