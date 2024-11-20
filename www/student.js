'use strict'

const switchView = document.querySelector('#switch')
switchView.addEventListener('click', function (event) {
  const codeView = document.querySelector('#code-view')
  const statsView = document.querySelector('#stats-view')
  if (statsView.style.display == 'none') {
    codeView.style.display = 'none'
    statsView.style.display = 'block'
    switchView.innerText = 'Show Code'
    let stats_interval = setInterval(getStats, 10000)
  } else {
    codeView.style.display = 'block'
    statsView.style.display = 'none'
    switchView.innerText = 'Show Stats'
    clearInterval(stats_interval)
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

function sendIntialData(){  
  let startCode = ""
  let desiredOutput = ""
  let classCode = ""
  let assignmentCode = ""
  
  //Pull class and assignment code out of link
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))
    startCode = urlList[0]
    desiredOutput = urlList[1]
    classCode = urlList[2]
    assignmentCode = urlList[3] 
  }
  //Call API to send class code to the database
  fetch ('/api/section', {
    method: 'POST',
    headers: {
      'Content-Type': 'application',
    },
    body: JSON.stringify({ txt_section_name: classCode }),
  })
  .then((response) => response.json())
  //Call API to send assignment code to the database
  fetch ('/api/exercise', {
    method: 'POST',
    headers: {
      'Content-Type': 'application',
    },
    body: JSON.stringify({ txt_exercise_name: assignmentCode, txt_starting_code: startCode, txt_desired_output: desiredOutput })
  })
  //Call API to send username to the database 
  fetch ('/api/student', {
    method: 'POST',
    headers: {
      'Content-Type': 'application',
    },
    body: JSON.stringify({ txt_student_name: userName })
  })
}
