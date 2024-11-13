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
function updateSharing() {
  const codeText = document.querySelector('#code-area').value
  const outputText = document.querySelector('#output-text').value

  const base64String = btoa(JSON.stringify([codeText, outputText]))

  const classCode = document.querySelector('#class-code').value

  const url =
    location.origin +
    location.pathname +
    'student.html' +
    `#${base64String}` +
    `#${classCode}`

  if (document.querySelector('#share-type').value == 'share') {
    document.querySelector('#share-text').value = url
  } else {
    const embedCode = `<iframe src="${url}" width="100%" height="800" frameborder="0" allowfullscreen></iframe>`
    document.querySelector('#share-text').value = embedCode
  }
}
window.addEventListener('load', updateSharing)

document.querySelectorAll('textarea,select').forEach(e => {
  e.addEventListener('input', updateSharing)
})

const linkDisplay = document.querySelector('#copy')
linkDisplay.addEventListener('click', function (event) {
  event.preventDefault()
  navigator.clipboard
    .writeText(document.querySelector('#share-text').value)
    .then(
      function () {
        console.log('Copied link successfully!')
        document.querySelector('#copy').innerHTML = 'Copied!'

        setTimeout(() => {
          document.querySelector('#copy').innerHTML = 'Copy'
        }, 1000)
      },
      function () {
        console.log('Failed to copy link')
      },
    )
})

const linkClass = document.querySelector('#link-to-class')
linkClass.addEventListener('click', function (event) {
  updateSharing()
})
