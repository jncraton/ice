importScripts('https://cdn.jsdelivr.net/pyodide/v0.26.3/full/pyodide.js')

async function configurePyodide() {
  self.pyodide = await loadPyodide()
  self.pythonConsoleString = ''
  // Override Python's input function to simulate user input via a custom handler
  self.pyodide.globals.set('input', promptText => {
    return new Promise(resolve => {
      // Send a message to the main thread to display the input prompt
      self.postMessage({
        type: 'input-request',
        message: promptText,
      })

      // Store resolve function to resolve when user input is received
      self._resolveInput = resolve
    })
  })

  // Handle messages from the main thread, including user input
  self.onmessage = function (event) {
    if (event.data.type === 'user-input') {
      // Resolve the input promise when user input is received
      if (self._resolveInput) {
        self._resolveInput(event.data.input) // Resolves the promise from input()
      }
    }
  }
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
    // Return the error message to student.js
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
