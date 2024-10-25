// Load data from URL
function loadDefaultData() {
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))
    
    document.querySelector('#code-area').value = urlList[0]
    document.querySelector('#output-text').value = urlList[1]
  }
}
loadDefaultData()

let codeExecuting = false;
const codeWorker = new Worker("/src/worker.js")
const runButton = document.querySelector("#run-button")

runButton.addEventListener("click", function () {
  const studentCode = document.querySelector("#code-area").value
  runButton.disabled = true

  console.log("Posting message")
  codeWorker.postMessage({
    type: "run",
    language: "python",
    code: studentCode,
  })

  // runPythonCode(studentCode).then(
  //   (codeResult) => {
  //     console.log("Code finished running, getting result")
  //     // result = codeResultPromise.pa
  //     document.querySelector('#code-output').innerHTML = codeResult
  //   }
  // )


  // pythonWorker.postMessage("First message")

//   const codeResult = runPythonCode(studentCode)
//   console.log("Code finished running.")
//   document.querySelector('#code-output').innerHTML = codeResult
})

codeWorker.addEventListener("message", function (msg) {
  console.log("Message received")

  if (msg.data.type === "result") {
    document.querySelector('#code-output').innerHTML = msg.data.result
    runButton.disabled = false
  }
})