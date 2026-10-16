// Circuit 9: cancelling through gates on the SAME qubit
// T on the CNOT control commutes with the CNOT  -> T ... Tdg cancel
// X on the CNOT target commutes with the CNOT   -> X ... X cancel
// Two CNOTs with the same control commute       -> CX(0,1) ... CX(0,1) cancel
// S on a CZ qubit commutes with the CZ           -> S ... Sdg cancel
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];

t q[0];
cx q[0],q[1];
tdg q[0];

x q[1];
cx q[0],q[1];
x q[1];

cx q[0],q[1];
cx q[0],q[2];
cx q[0],q[1];

s q[2];
cz q[1],q[2];
sdg q[2];
