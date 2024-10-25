'use strict'

// Load data from URL
function loadDefaultData() {
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))

    document.querySelector('#code-area').value = urlList[0]
    document.querySelector('#output-text').value = urlList[1]
  }
}
loadDefaultData()

// Make check output button function
document.querySelector('#run').addEventListener('click', function () {
  const codeText = document.querySelector('#code-area').value
  const outputText = document.querySelector('#output-text').value
  const label = document.querySelector('#checkCodeResult')
  if (codeText === outputText) {
    label.textContent = "Correct";
  } else {
    label.textContent = "Does not match target output";
  }
})