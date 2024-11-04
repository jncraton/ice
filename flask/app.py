from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def instructor_page():
    return render_template("index.html")


@app.route("/student")
def student_page():
    return render_template("student.html")
