// Load data from URL
function loadDefaultData() {
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))
    
    document.querySelector('#code-area').value = urlList[0]
    document.querySelector('#output-text').value = urlList[1]
  }
}
loadDefaultData()

document.querySelector("#run-button").addEventListener("click", function (event) {
  const studentCode = document.querySelector("#code-area").value
  const codeResultPromise =  runPythonCode(studentCode).then(
    (codeResult) => {
      console.log("Code finished running, getting result")
      // result = codeResultPromise.pa
      document.querySelector('#code-output').innerHTML = codeResult
    }
  )
})


// Run python code and print the output
async function runPythonCode(code) {
  console.log(`Running code ${code}...`)
  const pyodide = await loadPyodide()

  let pythonConsoleString = "Results below: "
  pyodide.setStdout({ batched: function (msg) { pythonConsoleString += `\n${msg}` } })

  const pythonOutput = pyodide.runPython(code)
  pythonConsoleString += `\n\nReturned ${pythonOutput}`

  console.log(`Code resulted in ${pythonConsoleString}`)

  return pythonConsoleString
}
// runStudentPython()