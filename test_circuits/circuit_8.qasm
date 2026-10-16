// Circuit 8: single-qubit gate merging
// H X H = Z   (3 gates -> 1)
// T T   = S   (2 gates -> 1)
// S S   = Z   (2 gates -> 1)
// X Y Z = identity (removed completely)
OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];

h q[0];
x q[0];
h q[0];

t q[1];
t q[1];

s q[2];
s q[2];

x q[3];
y q[3];
z q[3];
