var editor = ace.edit("editor");
editor.session.setMode("ace/mode/python");
editor = ace.edit("editor");
editor.setOption("wrap", true);
editor.setOption("fontSize", 12);
editor.setTheme("ace/theme/terminal");
editor.setHighlightActiveLine(false);
editor.focus();

function goto(lineNumber) {
    editor.gotoLine(lineNumber);
    editor.setHighlightActiveLine(true);
}

async function postForm() {

    const form = new FormData(document.getElementById("codeform"));

    const response = await fetch("/", {
        method: "POST",
        body: form,
    });

    const data = await response.text();

    if (response.ok) {
        document.getElementById("results").innerHTML = data;
    } else {
        throw new Error(data.error);
    }
}

editor.getSession().on("change", function (e) {
    document.getElementById("code").value = editor.getValue();
    postForm();
});

document.getElementById("mode-select").addEventListener("click", (e) => {
    let container = document.getElementById("theme-area");
    let logo = document.getElementById("logo");
    if (e.target.matches(':checked')) {
        editor.setTheme("ace/theme/katzenmilch");
        container.classList.add("light");
        container.classList.remove("dark");
        logo.src = "https://codeinstitute.s3.amazonaws.com/assets/logo.png";
    } else {
        editor.setTheme("ace/theme/terminal");
        container.classList.add("dark");
        container.classList.remove("light");
        logo.src = "https://codeinstitute.s3.amazonaws.com/assets/logo_white.png";
    }
});

document.getElementById("editor").addEventListener("click", (e) => {
    editor.setHighlightActiveLine(false);
});

postForm();