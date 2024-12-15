import { searchFormulas, getFormulaDetails } from './api.js';
import { renderSearchResults } from './components/resultsRenderer.js';
import { updateMathPreview } from './utils/mathJaxUtils.js';
import { insertAtCursor } from './utils/keyboardUtils.js';
import { createFormulaDetailsSection, updateFormulaDetails } from './components/formulaDetails.js';
import { createVariableNamesToggle, getVariableNamesState } from './components/variableNamesToggle.js';

// DOM Elements
const elements = {
  latexInput: document.getElementById('latex-input'),
  preview: document.getElementById('preview'),
  mathKeyboard: document.querySelector('.math-keyboard'),
  searchResults: document.getElementById('search-results'),
  searchButton: document.getElementById('search-button'),
  editorContainer: document.querySelector('.editor-container')
};

// Create and insert formula details section
const formulaDetailsSection = createFormulaDetailsSection();
elements.editorContainer.insertBefore(formulaDetailsSection, elements.editorContainer.firstChild);

// Create and insert variable names toggle
const variableNamesToggle = createVariableNamesToggle();
elements.editorContainer.querySelector('.input-section').insertBefore(
  variableNamesToggle,
  elements.searchButton
);

// Formula click handler
async function handleFormulaClick(latex) {
  const details = await getFormulaDetails(latex, elements.latexInput.value);
  updateFormulaDetails(formulaDetailsSection, details);
}

// Search handler
async function handleSearch() {
  elements.searchButton.disabled = true;
  elements.searchButton.textContent = 'Searching...';
  
  try {
    const results = await searchFormulas(
      elements.latexInput.value,
      getVariableNamesState()
    );
    renderSearchResults(results, elements.searchResults, handleFormulaClick);
  } finally {
    elements.searchButton.disabled = false;
    elements.searchButton.textContent = 'Search';
  }
}

// Event Handlers
function handleKeyboardClick(e) {
  if (e.target.tagName === 'BUTTON') {
    const latex = e.target.dataset.latex;
    const cursorOffset = parseInt(e.target.dataset.cursorOffset) || latex.length;
    const newValue = insertAtCursor(elements.latexInput, latex, cursorOffset);
    updateMathPreview(elements.preview, newValue);
  }
}

function handleInputChange() {
  updateMathPreview(elements.preview, elements.latexInput.value);
}

// Event Listeners
elements.mathKeyboard.addEventListener('click', handleKeyboardClick);
elements.latexInput.addEventListener('input', handleInputChange);
elements.searchButton.addEventListener('click', handleSearch);

// Initial preview
handleInputChange();