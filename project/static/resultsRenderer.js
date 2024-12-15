// Results display functionality
export function renderSearchResults(results, container) {
  container.innerHTML = '';
  console.error('renderSearchResults_results', results)
  console.error('renderSearchResults_container', container)
  
  if (!results.length) {
    container.innerHTML = '<p class="no-results">No similar formulas found</p>';
    return;
  }

  results.forEach(([formula, score1, score2]) => {
    const resultItem = document.createElement('div');
    resultItem.className = 'result-item';
    
    const formulaDisplay = document.createElement('div');
    formulaDisplay.className = 'formula-display';
    formulaDisplay.textContent = `$$${formula}$$`;
    
    const scores = document.createElement('div');
    scores.className = 'scores';
    scores.textContent = `Similarity: ${score1}%, Relevance: ${score2}%`;
    
    resultItem.appendChild(formulaDisplay);
    resultItem.appendChild(scores);
    container.appendChild(resultItem);
    
    // Render the math formula
    MathJax.typesetPromise([formulaDisplay]);
  });
}