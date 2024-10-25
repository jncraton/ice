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

  let result = await pyodide.runPythonAsync(code)

  return self.pythonConsoleString + `\n\n${result}`
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
