# Research Direction

## Current Topic

Quantum Compiler Optimization:
Gate Scheduling and Gate Cancellation

## Current Implemented Techniques

- Adjacent gate cancellation
- Inverse gate cancellation
- Basic commutation-based cancellation
- Basic gate scheduling
- Benchmark comparison with Qiskit

## Proposed Research Direction

State- and Hardware-Aware Commutation Cancellation
with Multi-Gate Lookahead

## Research Hypothesis

A cancellation method that considers gate commutation,
gate cost, and multiple future gates may reduce circuit
cost more effectively than simple local cancellation.

## Important Cost Factors

- Total gate count
- Circuit depth
- Two-qubit gate count
- T-count
- SWAP count
- Weighted gate cost
- Compilation time

## Novelty Status

The current implementation is a baseline.
The proposed lookahead and hardware-aware method
must be compared with existing literature before
claiming novelty.

## Future Work

1. Review related quantum compiler papers.
2. Identify limitations in existing cancellation methods.
3. Implement multi-gate lookahead.
4. Add hardware-aware gate cost.
5. Compare against Qiskit.
6. Analyze results.