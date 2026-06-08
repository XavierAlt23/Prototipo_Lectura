export function isValidPredictionText(text) {
  const length = text.trim().length;
  return length >= 5 && length <= 500;
}
