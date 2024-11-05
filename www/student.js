'use strict'

// Load data from URL
function loadDefaultData() {
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))

    document.querySelector('#code-area').value = urlList[0]
    document.querySelector('#target-text').value = urlList[1]
  }
}
loadDefaultData()

// Make check output button function
function checkOutput(output) {
  let targetText = document.querySelector('#target-text').value
  targetText = formatString(targetText)
  output = formatString(output)
  const label = document.querySelector('#check-code-result')
  if (output === targetText) {
    label.textContent = 'Correct   ✔'
    label.classList.add('labelCorrect')
    label.classList.remove('labelIncorrect')
  } else {
    label.textContent = 'Does not match target output   ❌'
    label.classList.add('labelIncorrect')
    label.classList.remove('labelCorrect')
  }
}

//Removes leading and trailing white space from string
function formatString(val) {
  val.trim()
  const withoutLineBreaks = val.replace(/[\r\n]/gm, '')
  return withoutLineBreaks
}
