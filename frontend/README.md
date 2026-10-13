# QRoute Lab frontend

A React + Vite dashboard for the quantum circuit optimizer research prototype.

## Run locally

1. Install Node.js 18 or newer.
2. Open a terminal in this `frontend` directory.
3. Install dependencies:

   ```bash
   npm install
   ```

4. Start the development server:

   ```bash
   npm run dev
   ```

5. Open the local URL printed by Vite (usually `http://localhost:5173`).

To check a production build, run `npm run build`.

## Data and backend integration

- `src/data/benchmarks.js` contains the benchmark labels, metric definitions and only the supplied/verified `mixed` benchmark result values.
- `src/services/resultsService.js` is the single data-access layer. The current default is mock mode. Other benchmark selections intentionally show an unavailable state rather than invented metrics.
- `src/components/` contains the comparison table, metric chart and illustrative input-circuit preview.

The Python `get_benchmark_results()` function is not directly callable from a browser. To integrate it, expose a small HTTP endpoint such as `GET /api/benchmarks/:benchmark` that returns the backend dictionary as JSON, then set `VITE_RESULTS_MODE=api` and `VITE_API_BASE_URL` in a `.env` file. The endpoint must handle CORS for the Vite origin. Do not point the frontend at the Python function itself; browsers require an HTTP interface.

The circuit diagram is an illustrative view of each benchmark's input gate sequence, not a visualization of the optimized output. Hardware-aware routing and state-aware simplification are clearly marked as planned work. Weighted cost is the existing heuristic (SWAP=10, other two-qubit gate=5, T/T†=3, other gates=1), not a hardware-calibrated estimate.
