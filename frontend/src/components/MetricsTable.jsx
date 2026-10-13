import React from 'react';
import { METRICS } from '../data/benchmarks';
import { Info } from 'lucide-react';

const COLUMNS = [
  { key: 'original', label: 'Original', className: 'col-original' },
  { key: 'optimized', label: 'Our optimizer', className: 'col-ours' },
  { key: 'qiskit', label: 'Qiskit baseline', className: 'col-qiskit' },
];

export default function MetricsTable({ results }) {
  return <section className="panel metrics-panel">
    <div className="panel-heading"><div><div className="eyebrow">RESULTS</div><h2>Metric comparison</h2></div><span className="soft-tag">Lower is better*</span></div>
    <div className="table-wrap"><table className="metrics-table"><thead><tr><th>Metric</th>{COLUMNS.map((c) => <th key={c.key}><span className={`column-marker ${c.className}`} />{c.label}</th>)}</tr></thead>
      <tbody>{METRICS.map((metric) => <tr key={metric.key}><td><span className="metric-name">{metric.label}<span className="metric-help" title={metric.help}><Info size={13} /></span></span><span className="metric-description">{metric.help}</span></td>{COLUMNS.map((column) => <td key={column.key} className="numeric-cell">{results[column.key]?.[metric.key] ?? '—'}</td>)}</tr>)}</tbody>
    </table></div>
    <p className="footnote">*Metrics are useful indicators, not interchangeable objectives. Weighted cost is a project heuristic, not a hardware-calibrated runtime estimate.</p>
  </section>;
}
