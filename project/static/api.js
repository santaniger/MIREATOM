// API related functions
export async function searchFormulas(latexCode, useNames) {
  try {
    const response = await fetch('/list/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        latex: latexCode,
        use_names: useNames 
      })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.list || [];
  } catch (error) {
    console.error('Error fetching results:', error);
    return [];
  }
}

export async function getFormulaDetails(latex, baseLatex) {
  try {
    const formData = new FormData();
    formData.append('text', latex);
    formData.append('base_latex', baseLatex);

    const response = await fetch('/info/', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching formula details:', error);
    return null;
  }
}