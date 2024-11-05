from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route("/")
def instructor_page():
    return send_from_directory("static", "index.html")


@app.route("/student")
def student_page():
    return send_from_directory("static", "student.html")
