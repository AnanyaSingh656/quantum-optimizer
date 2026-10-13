import React from 'react';
import { BENCHMARKS } from '../data/benchmarks';

const CIRCUITS = {
  mixed: [
    { q: 'q₀', gates: ['H', 'H', 'H', 'H', 'CX', 'T', 'T†'] },
    { q: 'q₁', gates: ['X', '·', '·', '·', '●', '·', 'SWAP'] },
    { q: 'q₂', gates: ['·', 'H', 'X', 'H', 'CX', '·', 'SWAP'] },
  ],
  adjacent: [ { q: 'q₀', gates: ['H', 'H'] }, { q: 'q₁', gates: ['X', 'X'] } ],
  commutation: [ { q: 'q₀', gates: ['H', '·', 'H'] }, { q: 'q₁', gates: ['·', 'X', '·'] } ],
  inverse_gates: [ { q: 'q₀', gates: ['T', 'T†'] }, { q: 'q₁', gates: ['S', 'S†'] } ],
  two_qubit: [ { q: 'q₀', gates: ['●', '●'] }, { q: 'q₁', gates: ['X', 'X', 'SWAP'] }, { q: 'q₂', gates: ['·', '·', 'SWAP'] } ],
};

function Gate({ label }) {
  if (label === '·') return <span className="wire-dot" />;
  if (label === '●') return <span className="control-dot" />;
  const kind = label === 'CX' || label === 'SWAP' ? 'gate-two' : label.includes('†') ? 'gate-inverse' : 'gate-single';
  return <span className={`gate ${kind}`}>{label}</span>;
}

export default function CircuitPreview({ benchmark }) {
  const rows = CIRCUITS[benchmark] || CIRCUITS.mixed;
  const info = BENCHMARKS.find((item) => item.id === benchmark);
  const max = Math.max(...rows.map((row) => row.gates.length));
  return <section className="panel circuit-panel">
    <div className="panel-heading">
      <div><div className="eyebrow">CIRCUIT EXPLORER</div><h2>Input circuit preview</h2></div>
      <span className="soft-tag">Illustrative</span>
    </div>
    <p className="panel-subtitle">Gate sequence from the benchmark definition. This is not a rendered post-optimization circuit.</p>
    <div className="circuit-canvas">
      {rows.map((row) => <div className="wire-row" key={row.q}>
        <span className="qubit-label">{row.q}</span><div className="wire-track" style={{ '--slots': max }}>
          {Array.from({ length: max }, (_, i) => <div className="wire-slot" key={i}><Gate label={row.gates[i] || '·'} /></div>)}
        </div>
      </div>)}
    </div>
    <div className="circuit-legend"><span><i className="legend-square single" />Single-qubit</span><span><i className="legend-square two" />Multi-qubit / routing gate</span><span><i className="legend-square inverse" />Inverse gate</span></div>
    <div className="circuit-foot"><span className="status-dot" />{info?.qubits ?? rows.length} qubits · {info?.label ?? 'Benchmark'}</div>
  </section>;
}
