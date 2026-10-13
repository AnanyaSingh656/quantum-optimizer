import { MOCK_RESULTS } from '../data/benchmarks';

// Integration seam: keep all result fetching here, not in UI components.
// Current mode uses only supplied demo values. Set VITE_RESULTS_MODE=api when
// an HTTP adapter exists that serves GET /api/benchmarks/:benchmark.
const MODE = import.meta.env.VITE_RESULTS_MODE || 'mock';
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function getBenchmarkResults(benchmark) {
  if (MODE === 'api') {
    const response = await fetch(`${API_BASE_URL}/api/benchmarks/${encodeURIComponent(benchmark)}`);
    if (!response.ok) throw new Error(`Backend request failed (${response.status}).`);
    const data = await response.json();
    if (data.status !== 'success' || !data.results) throw new Error(data.message || 'The backend returned an invalid result.');
    return { ...data, source: 'api' };
  }

  // Small delay makes the loading state visible during a demo.
  await new Promise((resolve) => setTimeout(resolve, 350));
  if (!MOCK_RESULTS[benchmark]) {
    return { status: 'unavailable', benchmark, message: 'Verified metrics for this benchmark are not included in the mock dataset yet. Connect the Python backend to calculate them live.' };
  }
  return MOCK_RESULTS[benchmark];
}
