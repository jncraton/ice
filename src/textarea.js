// Allow user to type tabs in code area
// This is in its own file so code is not duplicated across index.js and student.js
codeArea = document.querySelector("#code-area")
codeArea.addEventListener("keydown", function (event) {
    if (event.key === "Tab") {
        event.preventDefault()
        
        codeArea.setRangeText("\t", codeArea.selectionStart, codeArea.selectionEnd, "end")
    }
})