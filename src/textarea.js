codeArea = document.querySelector("#code-area")
codeArea.addEventListener("keydown", function (event) {
    if (event.key === "Tab") {
        event.preventDefault()
        
        codeArea.setRangeText("   ", codeArea.selectionStart, codeArea.selectionEnd, "end")
    }
})