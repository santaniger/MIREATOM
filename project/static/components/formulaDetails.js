import { renderMathFormula } from '../utils/mathJaxUtils.js';

export function createFormulaDetailsSection() {
  const section = document.createElement('div');
  section.className = 'formula-details-section';
  section.style.display = 'none';
  
  section.innerHTML = `
    <div class="formula-details-content">
      <div class="formula-latex"></div>
      <div class="formula-source"></div>
      <div class="formula-description"></div>
    </div>
  `;
  
  return section;
}

export function updateFormulaDetails(container, details) {
  if (!details) {
    container.style.display = 'none';
    return;
  }

  const latexElement = container.querySelector('.formula-latex');
  const sourceElement = container.querySelector('.formula-source');
  const descriptionElement = container.querySelector('.formula-description');

  latexElement.textContent = `$$${details.LaTeX}$$`;
  sourceElement.textContent = `Файл: ${details.link}`;
  descriptionElement.textContent = details.legend;

  renderMathFormula(latexElement);
  container.style.display = 'block';
}