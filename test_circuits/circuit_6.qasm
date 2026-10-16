// Circuit 6: needs 2 rounds
// Round 1 removes T/Tdg, which brings the two H gates on q[0]
// next to each other (only X on q[1] between them).
// Round 2 then cancels the H gates.
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];

h q[0];
t q[0];
tdg q[0];
x q[1];
h q[0];
