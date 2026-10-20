// Circuit 35: Stabilizer measurement rounds
// Two rounds of X- and Z-type stabilizer checks on 4 data qubits and 5 ancillas (surface-code style).
// 9 qubits, 28 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[9];
h q[4];
cx q[4],q[0];
cx q[4],q[1];
cx q[4],q[2];
cx q[4],q[3];
h q[4];
cx q[0],q[5];
cx q[1],q[5];
cx q[2],q[6];
cx q[3],q[6];
cz q[0],q[7];
cz q[2],q[7];
cz q[1],q[8];
cz q[3],q[8];
h q[4];
cx q[4],q[0];
cx q[4],q[1];
cx q[4],q[2];
cx q[4],q[3];
h q[4];
cx q[0],q[5];
cx q[1],q[5];
cx q[2],q[6];
cx q[3],q[6];
cz q[0],q[7];
cz q[2],q[7];
cz q[1],q[8];
cz q[3],q[8];
