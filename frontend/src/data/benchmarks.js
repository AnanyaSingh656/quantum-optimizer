export const BENCHMARKS = [
  { id: 'mixed', label: 'Mixed operations', qubits: 3, description: 'Single-qubit gates, inverse pairs, CX gates and a SWAP.' },
  { id: 'adjacent', label: 'Adjacent cancellation', qubits: 2, description: 'Adjacent self-inverse gates designed to test cancellation.' },
  { id: 'commutation', label: 'Commutation', qubits: 2, description: 'Operations on separate qubits create a commutation opportunity.' },
  { id: 'inverse_gates', label: 'Inverse gates', qubits: 2, description: 'T/T† and S/S† inverse pairs.' },
  { id: 'two_qubit', label: 'Two-qubit gates', qubits: 3, description: 'CX cancellation and a SWAP operation.' },
];

// Only the mixed benchmark values below were supplied and verified for this demo.
// Do not infer or extrapolate metrics for the other benchmark circuits.
export const MOCK_RESULTS = {
  mixed: {
    status: 'success', benchmark: 'mixed', source: 'verified-demo',
    results: {
      original: { gate_count: 13, depth: 7, two_qubit_count: 3, t_count: 2, swap_count: 1, weighted_cost: 34 },
      optimized: { gate_count: 7, depth: 5, two_qubit_count: 3, t_count: 0, swap_count: 1, weighted_cost: 24 },
      qiskit: { gate_count: 4, depth: 3, two_qubit_count: 2, t_count: 0, swap_count: 0, weighted_cost: 12 },
    },
  },
};

export const METRICS = [
  { key: 'gate_count', label: 'Gate count', short: 'Gates', help: 'Total number of operations in the circuit. Lower is usually simpler.' },
  { key: 'depth', label: 'Circuit depth', short: 'Depth', help: 'Length of the longest dependency path; a rough measure of sequential execution layers.' },
  { key: 'two_qubit_count', label: 'Two-qubit gates', short: '2-qubit', help: 'Operations acting on two qubits, often costly on real hardware.' },
  { key: 't_count', label: 'T-count', short: 'T-count', help: 'Number of T and T† gates, relevant to fault-tolerant resource estimates.' },
  { key: 'swap_count', label: 'SWAP count', short: 'SWAPs', help: 'Number of explicit SWAP operations in the circuit.' },
  { key: 'weighted_cost', label: 'Weighted cost', short: 'Cost', help: 'Project heuristic: SWAP=10, other two-qubit gate=5, T/T†=3, other gate=1. Not a hardware-calibrated cost.' },
];
