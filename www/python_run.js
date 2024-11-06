'use strict'

const runButton = document.querySelector('#run-button')
const endButton = document.querySelector('#end-button')
const timeDisplayP = document.querySelector('#time-displayed')

endButton.disabled = true

// Create and configure a new web worker to run python code
function createCodeWorker() {
  const codeWorker = new Worker('/worker.js')

  codeWorker.addEventListener('message', function (msg) {
    console.log('Message received')

    if (msg.data.type === 'result') {
      document.querySelector('#code-output').innerHTML = msg.data.result
      runButton.disabled = false
      endButton.disabled = true
    }
  })

  return codeWorker
}

// Run python code in web worker and deal with run button
let codeWorker = createCodeWorker()
// let workerIsDead = false

// Run code when button pressed.
runButton.addEventListener('click', function () {
  //
  // if (workerIsDead) {
  //   codeWorker = createCodeWorker()
  // }
  const pythonCode = document.querySelector('#code-area').value
  runButton.disabled = true
  endButton.disabled = false

  console.log('Posting message')
  codeWorker.postMessage({
    type: 'run',
    language: 'python',
    code: pythonCode,
  })
})

endButton.addEventListener('click', function () {
  codeWorker.terminate()
  codeWorker = createCodeWorker() // send in the next worker

  runButton.disabled = false
  endButton.disabled = true
})
