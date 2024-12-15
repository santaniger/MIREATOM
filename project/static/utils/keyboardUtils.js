// Keyboard input handling utilities
export function insertAtCursor(input, textToInsert, cursorOffset) {
  const start = input.selectionStart;
  const end = input.selectionEnd;
  const text = input.value;
  const before = text.substring(0, start);
  const after = text.substring(end);
  
  input.value = before + textToInsert + after;
  
  // Calculate new cursor position
  const newPosition = start + cursorOffset;
  input.focus();
  input.setSelectionRange(newPosition, newPosition);
  
  return input.value;
}