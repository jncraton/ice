'use strict'

let stats_interval

const switchView = document.querySelector('#switch')
switchView.addEventListener('click', function (event) {
  const codeView = document.querySelector('#code-view')
  const statsView = document.querySelector('#stats-view')
  if (statsView.style.display == 'none') {
    codeView.style.display = 'none'
    statsView.style.display = 'block'
    switchView.innerText = 'Show Code'
    getStats()
    stats_interval = setInterval(getStats, 10000)
  } else {
    codeView.style.display = 'block'
    statsView.style.display = 'none'
    switchView.innerText = 'Show Stats'
    clearInterval(stats_interval)
  }
})
// Timer functionality
let timer_interval
let seconds = 0

let student_name = ''
document.querySelector('#start-button').addEventListener('click', function() {
	student_name = document.querySelector('#student-name').value
	if (student_name) {
		timer_interval = setInterval(timer, 1000)
		document.querySelector("#start-button").disabled = true
		document.querySelector("#student-name").disabled = true
  	document.querySelector('#code-area').disabled = false
    sendIntialData()
	}
	else {
		alert("Cannot start without student name")
	}
})

function timer() {
  let timerValue = new Date(1000 * seconds).toISOString().substr(11, 8)
  document.querySelector('#timer_val').innerHTML = timerValue
  seconds++
}

function sendIntialData(){  
  let startCode
  let desiredOutput
  let classCode
  let assignmentCode
  let teacherName
  
  //Pull class and assignment code out of link
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))
    startCode = urlList[0]
    desiredOutput = urlList[1]
    classCode = urlList[2]
    assignmentCode = urlList[3] 
    teacherName = urlList[4]
  }

  //Call API to send intial data to the database
  fetch ('/api/student_start', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ section_name: classCode, instructor_name: teacherName, 
      exercise_name: assignmentCode, exercise_starting_code: startCode, exercise_desired_output: desiredOutput, 
      student_name: student_name}),
    })
}


function sendFinalData(){
  //Call API to send intial data to the database
  fetch ('', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({})
  })
}


function getStats(){
  console.log("stats hit")
}