'use strict'

const switchView = document.querySelector('#switch')
switchView.addEventListener('click', function (event) {
  const codeView = document.querySelector('#code-view')
  const statsView = document.querySelector('#stats-view')
  if (statsView.style.display == 'none') {
    codeView.style.display = 'none'
    statsView.style.display = 'block'
    switchView.innerText = 'Show Code'
  } else {
    codeView.style.display = 'block'
    statsView.style.display = 'none'
    switchView.innerText = 'Show Stats'
  }
})
// Timer functionality
let timer_interval = setInterval(timer, 1000)
let seconds = 0

function timer() {
  let timerValue = new Date(1000 * seconds).toISOString().substr(11, 8)
  document.querySelector('#timer_val').innerHTML = timerValue
  seconds++
}

//Start button and Code Area
const startButton = document.querySelector('#start-button')
startButton.addEventListener('click', function () {
  document.querySelector('#code-area').disabled = false
  startButton.disabled = true
})