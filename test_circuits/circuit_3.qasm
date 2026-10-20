// Circuit 3: commutation (gates separated by a gate on another qubit)
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];

h q[0];
x q[1];
h q[0];
