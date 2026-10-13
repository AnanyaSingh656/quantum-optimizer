import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { METRICS } from '../data/benchmarks';
import React from 'react';
export default function MetricBars({ results, metric }) {
  const selected = METRICS.find((item) => item.key === metric) || METRICS[0];
  const data = [
    { name: 'Original', value: results.original?.[selected.key] ?? 0 },
    { name: 'Our optimizer', value: results.optimized?.[selected.key] ?? 0 },
    { name: 'Qiskit', value: results.qiskit?.[selected.key] ?? 0 },
  ];
  return <section className="panel chart-panel">
    <div className="panel-heading"><div><div className="eyebrow">AT A GLANCE</div><h2>Visual comparison</h2></div>
      <select className="chart-select" aria-label="Metric to chart" value={metric} onChange={(e) => window.dispatchEvent(new CustomEvent('metric-change', { detail: e.target.value }))}>{METRICS.map((m) => <option value={m.key} key={m.key}>{m.label}</option>)}</select>
    </div>
    <p className="panel-subtitle">{selected.help}</p>
    <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><BarChart data={data} margin={{ top: 12, right: 8, left: -16, bottom: 4 }} barCategoryGap="28%"><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e9edf5"/><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#64708a', fontSize: 11 }}/><YAxis allowDecimals={false} axisLine={false} tickLine={false} tick={{ fill: '#8993a8', fontSize: 11 }}/><Tooltip cursor={{ fill: '#f3f5fb' }} contentStyle={{ border: '1px solid #e7ebf3', borderRadius: 10, fontSize: 12 }}/><Bar dataKey="value" name={selected.label} fill="#6965f4" radius={[6, 6, 0, 0]} maxBarSize={48}/></BarChart></ResponsiveContainer></div>
  </section>;
}
