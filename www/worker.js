importScripts('https://cdn.jsdelivr.net/pyodide/v0.26.3/full/pyodide.js')

async function configurePyodide() {
  self.pyodide = await loadPyodide()
  self.pythonConsoleString = ''
  await self.pyodide.setStdout({
    batched: function (msg) {
      self.pythonConsoleString += `\n${msg}`
    },
  })
}

let configurePyodidePromise = configurePyodide()

// Run python code and print the output
async function runPythonCode(code) {
  console.log('Running code')

  await configurePyodidePromise
  self.pythonConsoleString = ''
  // let pythonConsoleString = ""
  // pyodide.setStdout({ batched: function (msg) { pythonConsoleString += `\n${msg}` } })

  try {
    let result = await pyodide.runPythonAsync(code)

    if (result == undefined) {
      return self.pythonConsoleString
    } else {
      return self.pythonConsoleString + `\n\nReturned: ${result}`
    }
  } catch (error) {
    // Return the error message to exercise.js
    return `Error: ${error.message}`
  }
}

this.addEventListener('message', function (msg) {
  console.log('Encountered message')
  if (msg.data.type === 'run' && msg.data.language === 'python') {
    runPythonCode(msg.data.code).then(function (result) {
      this.postMessage({
        type: 'result',
        result: result,
      })
    })
  }
})
