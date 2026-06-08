export function formatPercent(value) {
  if (value === null || value === undefined) return 'N/D';
  return `${(value * 100).toFixed(2)}%`;
}
