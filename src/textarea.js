codeArea = document.querySelector("#code-area")
codeArea.addEventListener("keydown", function (event) {
    if (event.key === "Tab") {
        event.preventDefault()
        
        codeArea.setRangeText("\t", codeArea.selectionStart, codeArea.selectionEnd, "end")
    }
})