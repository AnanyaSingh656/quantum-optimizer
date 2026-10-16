// Circuit 7: nested inverse pairs, needs 3 rounds
// Each round removes the innermost pair, exposing the next one.
OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];

t q[0];
s q[0];
z q[0];
z q[0];
sdg q[0];
tdg q[0];
