'use strict'

let executionTimeout, warningTimeout
let workerCompleted = false // Flag to track if worker finishes execution

const runButton = document.querySelector('#run-button')
const endButton = document.querySelector('#end-button')
const warningBox = document.querySelector('#warning-box')

// Load data from URL
function loadDefaultData() {
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))

    document.querySelector('#code-area').value = urlList[0]
    document.querySelector('#target-text').value = urlList[1]
  }
}
loadDefaultData()

// Create and configure a new web worker to run python code
function createCodeWorker() {
  const codeWorker = new Worker('worker.js')

  codeWorker.addEventListener('message', function (msg) {
    console.log('Message received')
    clearTimeout(executionTimeout) // clear timeout on successful execution
    workerCompleted = true // Mark worker as completed
    clearTimeout(warningTimeout) // clear warning timeout if worker finishes in time
    if (msg.data.type === 'result') {
      document.querySelector('#code-output').innerHTML = msg.data.result.trim()
      runButton.disabled = false
      endButton.disabled = true
      checkOutput(msg.data.result)
    }
  })

  return codeWorker
}

// Run python code in web worker and deal with run button
let codeWorker = createCodeWorker()

//Removes leading and trailing white space from string
function formatString(val) {
  val.trim()
  const withoutLineBreaks = val.replace(/[\r\n]/gm, '')
  return withoutLineBreaks
}

// Show warning box function
function showWarningBox() {
  if (warningBox && !workerCompleted) {
    // Only show if the worker is still running
    warningBox.classList.remove('warningHidden')
    warningBox.classList.add('warningVisible')
  }
}

// Hide warning box function
function hideWarningBox() {
  if (warningBox) {
    warningBox.classList.remove('warningVisible')
    warningBox.classList.add('warningHidden')
  }
}

// Make check output button function
function checkOutput(output) {
  let targetText = document.querySelector('#target-text').value
  if (!targetText) {
    return
  }

  targetText = formatString(targetText)
  output = formatString(output)
  const label = document.querySelector('#check-code-result')
  if (
    output === 'Error: Execution timed out. Possible infinite loop detected.'
  ) {
    label.textContent = 'Does not match target output   ❌'
    label.classList.add('labelIncorrect')
    label.classList.remove('labelCorrect')
  } else if (output === targetText) {
    label.textContent = 'Correct   ✔'
    label.classList.add('labelCorrect')
    label.classList.remove('labelIncorrect')
    clearInterval(timer_interval)
    document.querySelector('#submit-button').disabled = false
    sendFinalData()
  } else {
    label.textContent = 'Does not match target output   ❌'
    label.classList.add('labelIncorrect')
    label.classList.remove('labelCorrect')
  }
}

function sendFinalData() {
  let startCode
  let desiredOutput
  let classCode
  let assignmentCode
  let teacherName
  let studentName
  let finalCode

  //Pull information out of link
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))
    startCode = urlList[0]
    desiredOutput = urlList[1]
    classCode = urlList[2]
    assignmentCode = urlList[3]
    teacherName = urlList[4]
  }

  studentName = document.querySelector('#student-name').value
  finalCode = document.querySelector('#code-area').value

  //Call API to send intial data to the database
  fetch('/api/student_end', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      section_name: classCode,
      instructor_name: teacherName,
      exercise_name: assignmentCode,
      exercise_starting_code: startCode,
      exercise_desired_output: desiredOutput,
      student_name: studentName,
      student_final_code: finalCode,
    }),
  })
}

// Run code when button pressed.
runButton.addEventListener('click', function () {
  const pythonCode = document.querySelector('#code-area').value
  runButton.disabled = true
  endButton.disabled = false
  workerCompleted = false // Reset worker completion flag
  warningTimeout = setTimeout(showWarningBox, 2000)
  executionTimeout = setTimeout(() => {
    codeWorker.terminate()
    codeWorker = createCodeWorker() // reset the worker
    document.querySelector('#code-output').innerHTML =
      'Error: Execution timed out. Possible infinite loop detected.'
    runButton.disabled = false
    endButton.disabled = true
    hideWarningBox() // Hide warning when timeout occurs
    checkOutput('Error: Execution timed out. Possible infinite loop detected.')
  }, 20000) // Set timeout duration (20 seconds to match test)
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
  document.querySelector('#code-output').innerHTML =
    'Execution terminated by user.'
  runButton.disabled = false
  endButton.disabled = true
  clearTimeout(executionTimeout) // clear timeout on manual termination
  clearTimeout(warningTimeout) // Clear warning timeout if execution is stopped
  hideWarningBox() // Hide warning when execution is stopped
})
