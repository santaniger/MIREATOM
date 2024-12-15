// MathJax related utilities
export function renderMathFormula(element) {
  return MathJax.typesetPromise([element]);
}

export function updateMathPreview(previewElement, latex) {
  previewElement.textContent = '$$' + latex + '$$';
  return renderMathFormula(previewElement);
}