const addForm = (buttonElement) => {
  console.log(buttonElement.parentElement.parentElement.id)
  const currentForm = buttonElement.parentElement.parentElement.id
  // const formSet = document.getElementById('form_set')

  const formsCountElement = document.getElementById('id_form-TOTAL_FORMS')
  const formsCount = parseInt(formsCountElement.value)

  const emptyFormHtml = document.getElementById('empty-form').innerHTML
  const uniqueId = Date.now() + Math.random().toString(36).substr(2, 9);

  let newFormHtml = emptyFormHtml
    .replace(/__prefix__/g, formsCount)
    .replace('<div', `<div id="form-${uniqueId}"`)

  document.getElementById(currentForm).insertAdjacentHTML('afterend', newFormHtml)          
  formsCountElement.value = formsCount + 1
}

const removeForm = (buttonElement) => {
  const formToRemove = buttonElement.parentElement.parentElement;
  const formsCountElement = document.getElementById('id_form-TOTAL_FORMS');
  const formsCount = parseInt(formsCountElement.value);
  
  if (formsCount > 1) {
    formToRemove.remove();
    formsCountElement.value = formsCount - 1;
  }
}