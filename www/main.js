'use strict'

//Allow instructor to save output of their code using button
const saveOutput = document.querySelector('#save-output')
saveOutput.addEventListener('click', function () {
  const outputText = document.querySelector('#target-text')
  outputText.value = document.querySelector('#code-output').innerHTML
  outputText.dispatchEvent(new Event('input', { bubbles: true }))
})

// Make share button generate link to current page.
function updateSharing() {
  const codeText = document.querySelector('#code-area').value
  const outputText = document.querySelector('#target-text').value
  const classCode = document.querySelector('#class-code').value
  const assignmentCode = document.querySelector('#assignment-code').value
  const teacherName = document.querySelector('#instructor-name').value

  const base64String = btoa(
    JSON.stringify([
      codeText,
      outputText,
      classCode,
      assignmentCode,
      teacherName,
    ]),
  )

  const url =
    location.origin + location.pathname + 'student.html' + `#${base64String}`

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

//Display link and allow it to be copied
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

//Automatically updates link when class or assignment code is changed
document.querySelector('#class-code').addEventListener('input', updateSharing)
document
  .querySelector('#assignment-code')
  .addEventListener('input', updateSharing)
