// Variable names toggle component
export function createVariableNamesToggle() {
  const toggleContainer = document.createElement('div');
  toggleContainer.className = 'variable-names-toggle';
  
  toggleContainer.innerHTML = `
    <label class="toggle-switch">
      <input type="checkbox" id="useVariableNames">
      <span class="toggle-slider"></span>
      <span class="toggle-label">Учитывать названия переменных</span>
    </label>
  `;
  
  return toggleContainer;
}

export function getVariableNamesState() {
  return document.getElementById('useVariableNames').checked;
}