import { renderMathFormula } from '../utils/mathJaxUtils.js';

export function renderSearchResults(results, container, onFormulaClick) {
  container.innerHTML = '';
  
  if (!results || results.length === 0) {
    container.innerHTML = '<p class="no-results">Ничего не найдено</p>';
    return;
  }

  results.forEach(result => {
    const resultItem = document.createElement('div');
    resultItem.className = 'result-item';
    resultItem.style.cursor = 'pointer';
    
    const formulaDisplay = document.createElement('div');
    formulaDisplay.className = 'formula-display';
    formulaDisplay.textContent = `$$${result.latex_code}$$`;
    
    const scores = document.createElement('div');
    scores.className = 'scores';
    scores.textContent = `Процент визуальной схожести: ${result.raw_sccore}%, Если упростить: ${result.score}%`;
    
    resultItem.appendChild(formulaDisplay);
    resultItem.appendChild(scores);
    container.appendChild(resultItem);
    
    // Add click handler
    resultItem.addEventListener('click', () => onFormulaClick(result.latex_code));
    
    // Render the math formula
    renderMathFormula(formulaDisplay);
  });
}