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

// Make share button generate link to current page.
document.querySelector('#share').addEventListener('click', function () {
  const codeText = document.querySelector('#code-area').value
  const outputText = document.querySelector('#output-text').value

  const base64String = btoa(JSON.stringify([codeText, outputText]))

  const url =
    location.origin + location.pathname + 'student.html' + `#${base64String}`

  document.querySelector('#link-display').innerHTML = url
  document.querySelector('#link-display').href = url
})

const linkDisplay = document.querySelector('#link-display')
linkDisplay.addEventListener('click', function (event) {
  event.preventDefault()
  navigator.clipboard.writeText(linkDisplay.href).then(
    function () {
      console.log('Copied link successfully!')
    },
    function () {
      console.log('Failed to copy link')
    },
  )
})
