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

const saveOutput = document.querySelector('#save-output')
saveOutput.addEventListener('click', function () {
  document.querySelector('#output-text').value =
    document.querySelector('#code-output').innerHTML
})

// Make share button generate link to current page.
document.querySelector('#share').addEventListener('click', function () {
  const codeText = document.querySelector('#code-area').value
  const outputText = document.querySelector('#output-text').value

  const base64String = btoa(JSON.stringify([codeText, outputText]))

  const url =
    location.origin + location.pathname + 'student.html' + `#${base64String}`

  document.querySelector('#link-display').innerHTML = url
  document.querySelector('#copy-link').removeAttribute('hidden')
  document.querySelector('#link-display').href = url

  const embedCode = `<iframe src="${url}" width="100%" height="800" frameborder="0" allowfullscreen></iframe>`

  // Set the embed code in the textarea
  document.querySelector('#embed-code').value = embedCode
})

const linkDisplay = document.querySelector('#copy-link')
linkDisplay.addEventListener('click', function (event) {
  event.preventDefault()
  navigator.clipboard
    .writeText(document.querySelector('#link-display').innerHTML)
    .then(
      function () {
        console.log('Copied link successfully!')
        document.querySelector('#alert').innerHTML = 'Link copied to clipboard'
      },
      function () {
        console.log('Failed to copy link')
      },
    )
})
