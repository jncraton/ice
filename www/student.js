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
let timer_interval
let seconds = 0

function timer() {
  let timerValue = new Date(1000 * seconds).toISOString().substr(11, 8)
  document.querySelector('#timer_val').innerHTML = timerValue
  seconds++
}


let student_name = ''
document.querySelector('#start-button').addEventListener('click', function() {
	student_name = document.querySelector('#student-name').value
	if (student_name) {
		timer_interval = setInterval(timer, 1000)
		document.querySelector("#start-button").disabled = true
		document.querySelector("#student-name").disabled = true
  		document.querySelector('#code-area').disabled = false
		
	}
	else {
		alert("Cannot start without student name")
	}
})
