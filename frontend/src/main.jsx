import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  Activity, ArrowDownRight, Atom, CheckCircle2, ChevronDown,
  CircleHelp, Clock3, FlaskConical, GitCompareArrows, Layers3,
  Play, Route, ShieldCheck, Sparkles, TriangleAlert
} from 'lucide-react';

import { BENCHMARKS } from './data/benchmarks';
import { getBenchmarkResults } from './services/resultsService';
import MetricsTable from './components/MetricsTable';
import MetricBars from './components/MetricBars';
import CircuitPreview from './components/CircuitPreview';
import './styles.css';

function App() {
  const [benchmark, setBenchmark] = useState('mixed');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [metric, setMetric] = useState('gate_count');
  const [runNumber, setRunNumber] = useState(0);
  const [activeSection, setActiveSection] = useState('dashboard');

  useEffect(() => {
    const handler = (event) => setMetric(event.detail);
    window.addEventListener('metric-change', handler);
    return () => window.removeEventListener('metric-change', handler);
  }, []);

  async function runComparison(selectedBenchmark = benchmark) {
    setLoading(true);
    setError('');
    setData(null);

    try {
      const result = await getBenchmarkResults(selectedBenchmark);
      setData(result);
      setRunNumber((number) => number + 1);
    } catch (e) {
      setError(e?.message || 'Something went wrong while loading results.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    runComparison('mixed');
    // Load the supplied mixed benchmark when the page opens.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function navigateTo(sectionId) {
    setActiveSection(sectionId);
    document.getElementById(sectionId)?.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    });
  }

  function handleBenchmarkChange(event) {
    const selected = event.target.value;
    setBenchmark(selected);
    setData(null);
    setError('');
  }

  const successful = data?.status === 'success' && data?.results;

  const metricCards = successful
    ? [
        {
          title: 'Gate count',
          key: 'gate_count',
          icon: Layers3,
          note: `${data.results.original.gate_count - data.results.optimized.gate_count} fewer vs original`,
        },
        {
          title: 'Circuit depth',
          key: 'depth',
          icon: Activity,
          note: `${data.results.original.depth - data.results.optimized.depth} layers reduced`,
        },
        {
          title: 'Two-qubit gates',
          key: 'two_qubit_count',
          icon: GitCompareArrows,
          note: 'Connectivity-sensitive operations',
        },
        {
          title: 'Weighted cost',
          key: 'weighted_cost',
          icon: Sparkles,
          note: 'Project heuristic',
        },
      ]
    : [];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><Atom size={23} /></div>
          <div>
            <strong>QRoute <span>Lab</span></strong>
            <small>QUANTUM RESEARCH</small>
          </div>
        </div>

        <div className="side-section-label">WORKSPACE</div>

        <button
          type="button"
          className={`side-nav ${activeSection === 'dashboard' ? 'active' : ''}`}
          onClick={() => navigateTo('dashboard')}
        >
          <Activity size={17} />
          <span>Experiment dashboard</span>
          <span className="nav-pip" />
        </button>

        <button
          type="button"
          className={`side-nav muted ${activeSection === 'benchmarks' ? 'active' : ''}`}
          onClick={() => navigateTo('benchmarks')}
        >
          <FlaskConical size={17} />
          <span>Benchmarks</span>
          <span className="soon-tag">5</span>
        </button>

        <button
          type="button"
          className={`side-nav muted ${activeSection === 'routing-analysis' ? 'active' : ''}`}
          onClick={() => navigateTo('routing-analysis')}
        >
          <Route size={17} />
          <span>Routing analysis</span>
          <span className="planned-mini">Planned</span>
        </button>

        <div className="side-divider" />
        <div className="side-section-label">PROJECT STATUS</div>

        <div className="status-card">
          <div className="status-card-top">
            <span className="pulse-dot" />
            Prototype stage
          </div>
          <p>
            Baseline comparison is available. Research routing and state-aware
            passes are still in development.
          </p>
          <div className="progress-track"><span /></div>
          <div className="progress-label">
            <span>Current prototype</span>
            <b>In progress</b>
          </div>
        </div>

        <div className="sidebar-bottom">
          <div className="avatar">QC</div>
          <div>
            <strong>Third-year B.Tech CSE</strong>
            <small>Research project workspace</small>
          </div>
          <button
            type="button"
            className="icon-button help-icon"
            aria-label="Project information"
            title="Project information"
            onClick={() =>
              window.alert(
                'QRoute Lab is a research prototype. Hardware-aware routing and state-aware simplification are planned features.'
              )
            }
          >
            <CircleHelp size={16} />
          </button>
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div className="breadcrumb">
            Projects <span>/</span> <b>Quantum circuit optimizer</b>
          </div>
          <div className="topbar-right">
            <span className="prototype-label"><span />Prototype · Demo data</span>
            <div className="top-avatar" title="QRoute Lab">Q</div>
          </div>
        </header>

        <div className="page-content">
          <section className="hero">
            <div className="hero-copy">
              <div className="eyebrow hero-eyebrow">
                <span className="eyebrow-line" />
                RESEARCH EXPERIMENTS <span className="version-pill">v0.1</span>
              </div>
              <h1>State-Aware Quantum<br /><span>Circuit Routing</span></h1>
              <p className="hero-description">
                Compare circuit simplification approaches and track resource
                metrics across benchmark quantum circuits.
              </p>
              <div className="hero-meta">
                <span><ShieldCheck size={14} /> Semantics-preserving goal</span>
                <span><FlaskConical size={14} /> 5 benchmark circuits</span>
              </div>
            </div>
            <div className="hero-art" aria-hidden="true">
              <div className="orbit orbit-one" />
              <div className="orbit orbit-two" />
              <div className="orbit orbit-three" />
              <div className="atom-core"><Atom size={66} strokeWidth={1.1} /></div>
              <span className="node node-a" />
              <span className="node node-b" />
              <span className="node node-c" />
              <span className="node node-d" />
              <span className="art-label label-a">H</span>
              <span className="art-label label-b">CX</span>
              <span className="art-label label-c">T†</span>
            </div>
          </section>

          <section id="benchmarks" className="experiment-toolbar panel">
            <div className="selector-block">
              <label htmlFor="benchmark-select">BENCHMARK CIRCUIT</label>
              <div className="select-wrap">
                <select
                  id="benchmark-select"
                  value={benchmark}
                  onChange={handleBenchmarkChange}
                >
                  <optgroup label="Available benchmarks">
                    {BENCHMARKS.map((item) => (
                      <option value={item.id} key={item.id}>{item.label}</option>
                    ))}
                  </optgroup>
                </select>
                <ChevronDown size={16} />
              </div>
              <p>{BENCHMARKS.find((item) => item.id === benchmark)?.description}</p>
            </div>
            <div className="toolbar-action">
              <span className="last-run">
                <Clock3 size={14} />
                {runNumber ? `Run #${runNumber}` : 'Ready to run'}
              </span>
              <button
                type="button"
                className="run-button"
                onClick={() => runComparison(benchmark)}
                disabled={loading}
              >
                <Play size={15} fill="currentColor" />
                {loading ? 'Running comparison…' : 'Run comparison'}
              </button>
            </div>
          </section>

          {loading && (
            <section className="panel state-panel" aria-live="polite">
              <div className="spinner" />
              <div>
                <h3>Running benchmark comparison</h3>
                <p>Fetching the original, custom optimizer and Qiskit baseline metrics…</p>
              </div>
            </section>
          )}

          {error && !loading && (
            <section className="panel state-panel error-state" role="alert">
              <TriangleAlert size={22} />
              <div>
                <h3>Could not load results</h3>
                <p>{error}</p>
                <button type="button" className="text-button" onClick={() => runComparison(benchmark)}>
                  Try again
                </button>
              </div>
            </section>
          )}

          {!loading && !error && data?.status === 'unavailable' && (
            <section className="panel state-panel empty-state">
              <div className="empty-icon"><FlaskConical size={22} /></div>
              <div>
                <h3>No verified demo metrics for this circuit yet</h3>
                <p>{data.message}</p>
                <p className="state-tip">
                  Choose <b>Mixed operations</b> to view the supplied comparison,
                  or connect the Python backend through an HTTP API.
                </p>
              </div>
            </section>
          )}

          {!loading && successful && (
            <>
              <div className="results-intro">
                <div>
                  <h2>Experiment overview</h2>
                  <p>Results for <b>{BENCHMARKS.find((item) => item.id === benchmark)?.label}</b></p>
                </div>
                <div className="result-source">
                  <CheckCircle2 size={15} />
                  {data.source === 'api' ? 'Live backend result' : 'Verified supplied values'}
                </div>
              </div>

              <section className="metric-grid">
                {metricCards.map((card) => {
                  const Icon = card.icon;
                  const original = Number(data.results.original[card.key]) || 0;
                  const optimized = Number(data.results.optimized[card.key]) || 0;
                  const qiskit = Number(data.results.qiskit[card.key]) || 0;
                  const maxValue = Math.max(original, optimized, qiskit, 1);

                  return (
                    <div className="metric-card" key={card.key}>
                      <div className="metric-card-top">
                        <span>{card.title}</span>
                        <span className="metric-icon"><Icon size={17} /></span>
                      </div>
                      <div className="metric-value-row">
                        <strong>{data.results.optimized[card.key]}</strong>
                        <span className="metric-unit">
                          {card.key === 'weighted_cost' ? 'units' : 'count'}
                        </span>
                      </div>
                      <div className="metric-card-note">
                        <ArrowDownRight size={14} />{card.note}
                      </div>
                      <div className="metric-mini-bars" aria-label={`${card.title}: original ${original}, our optimizer ${optimized}, Qiskit ${qiskit}`}>
                        <i style={{ height: `${Math.max(12, (original / maxValue) * 28)}px` }} />
                        <i style={{ height: `${Math.max(8, (optimized / maxValue) * 28)}px` }} />
                        <i style={{ height: `${Math.max(6, (qiskit / maxValue) * 28)}px` }} />
                      </div>
                    </div>
                  );
                })}
              </section>

              <div className="content-grid">
                <MetricBars results={data.results} metric={metric} />
                <CircuitPreview benchmark={benchmark} />
              </div>

              <MetricsTable results={data.results} />

              <section className="research-note">
                <div className="research-note-icon"><ShieldCheck size={19} /></div>
                <div>
                  <strong>Interpretation note</strong>
                  <p>
                    These values describe this benchmark only. They do not establish
                    general superiority over Qiskit, and the current weighted cost is
                    a heuristic. Hardware-aware routing and state-aware simplification
                    are planned, not implemented.
                  </p>
                </div>
              </section>
            </>
          )}

          <section id="routing-analysis" className="roadmap-section">
            <div className="roadmap-heading">
              <div>
                <div className="eyebrow">IMPLEMENTATION STATUS</div>
                <h2>What’s implemented — and what’s next</h2>
              </div>
              <span className="roadmap-caption">Research roadmap</span>
            </div>

            <div className="roadmap-grid">
              <div className="roadmap-item done">
                <div className="roadmap-icon"><CheckCircle2 size={18} /></div>
                <div>
                  <span className="roadmap-state">IMPLEMENTED</span>
                  <h3>Gate simplification</h3>
                  <p>Basic inverse-gate cancellation and commutation-based simplification.</p>
                </div>
              </div>
              <div className="roadmap-item done">
                <div className="roadmap-icon"><CheckCircle2 size={18} /></div>
                <div>
                  <span className="roadmap-state">IMPLEMENTED</span>
                  <h3>Metrics &amp; baseline</h3>
                  <p>Gate count, depth, two-qubit count, T-count, SWAP count and heuristic cost.</p>
                </div>
              </div>
              <div className="roadmap-item planned">
                <div className="roadmap-icon"><Route size={18} /></div>
                <div>
                  <span className="roadmap-state">PLANNED</span>
                  <h3>Hardware-aware routing</h3>
                  <p>Map circuit interactions to a specified hardware connectivity graph.</p>
                </div>
              </div>
              <div className="roadmap-item planned">
                <div className="roadmap-icon"><Sparkles size={18} /></div>
                <div>
                  <span className="roadmap-state">PLANNED</span>
                  <h3>State-aware simplification</h3>
                  <p>Apply only justified rewrites backed by explicit state information and correctness checks.</p>
                </div>
              </div>
            </div>
          </section>

          <footer className="footer">
            <span>QRoute Lab <span className="footer-separator">·</span> Research prototype</span>
            <span>Built for experimental comparison, not a correctness certificate.</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
