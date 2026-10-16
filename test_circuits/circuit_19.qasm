// Circuit 19: Bernstein-Vazirani, 7-bit secret
// Bernstein-Vazirani algorithm for the secret string 1011011 (oracle made of CNOTs).
// 8 qubits, 22 gates
OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
x q[7];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
h q[6];
h q[7];
cx q[0],q[7];
cx q[2],q[7];
cx q[3],q[7];
cx q[5],q[7];
cx q[6],q[7];
h q[0];
h q[1];
h q[2];
h q[3];
h q[4];
h q[5];
h q[6];
h q[7];
