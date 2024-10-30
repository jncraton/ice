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
function checkOutput(output){
  let targetText = document.querySelector('#target-text').value
  console.log(targetText)
  console.log(output)
  targetText = formatString(targetText)
  output = formatString(output)
  const label = document.querySelector('#check-code-result')
  if (output == targetText) {
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
function formatString(val){
  val.strip()
  return val
}

// Create and configure a new web worker to run python code
function createCodeWorker() {
  const codeWorker = new Worker('./worker.js')

  codeWorker.addEventListener('message', function (msg) {
    console.log('Message received')

    if (msg.data.type === 'result') {
      document.querySelector('#code-output').innerHTML = msg.data.result
      runButton.disabled = false
      endButton.disabled = true
      checkOutput(msg.data.result)
    }
  })

  return codeWorker
}

// Run python code in web worker and deal with run button
let codeWorker = createCodeWorker()

// get HTML elements
const runButton = document.querySelector('#run-button')
const endButton = document.querySelector('#end-button')
const timeDisplayP = document.querySelector('#time-displayed')

// Run code when button pressed.
runButton.addEventListener('click', function () {
  const studentCode = document.querySelector('#code-area').value
  runButton.disabled = true
  endButton.disabled = false

  console.log('Posting message')
  codeWorker.postMessage({
    type: 'run',
    language: 'python',
    code: studentCode,
  })
})

endButton.addEventListener('click', function () {
  codeWorker.terminate()
  codeWorker = createCodeWorker() // send in the next worker

  runButton.disabled = false
  endButton.disabled = true
})
