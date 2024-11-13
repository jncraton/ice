"""
    Flask server for running the API for the database and web server for the application. 

    Currently provides routes to all static files in the `www` directory
"""

import sqlite3
import os.path
from flask import Flask, request, g
from datetime import datetime
import time

app = Flask(__name__, static_folder="../www")

DATABASE_PATH = "../app/db/ice-database.db"


# Set up database
def get_db():
    """
    Establishes a connection to the database. Requires an app context to run.
    See https://flask.palletsprojects.com/en/stable/patterns/sqlite3/ for more details.
    """
    db = getattr(g, "_database", None)
    if db is None:
        if os.path.isfile(DATABASE_PATH):
            # If the database file exists, load it. Otherwise, init the database.
            db = g._database = sqlite3.connect(DATABASE_PATH)
        else:
            db = g._database = sqlite3.connect(DATABASE_PATH)
            with app.open_resource("db/schema.sql") as f:
                db.cursor().executescript(f.read().decode("utf-8"))
            db.commit()

    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(exception):
    """Closes the connection to the database when the app context is destroyed."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.commit()
        db.close()


def query_db(statement, args=(), one=False):
    """Executes a SQL statement against the database and returns the results."""
    cur = get_db().execute(statement, args)
    results = cur.fetchall()
    cur.close()

    return (results[0] if results else None) if one else results


# Web server routing
@app.route("/")
def serve_root():
    """Return index.html when the page is first loaded"""
    return app.send_static_file("index.html")


@app.route("/<filename>.html")
@app.route("/<filename>.js")
@app.route("/<filename>.css")
def serve_site(filename):
    """Correctly route all elements within the `www` directory"""
    # pylint: disable=unused-argument
    return app.send_static_file(request.path.lstrip("/"))


# API routing
@app.route("/api/student}")
def api_student():
    """Handle GET and POST requests made to /api/student.
    On a GET request, returns an array of dictionaries which represent the results of the query made
    On a POST request, adds the designated exercise to the database and returns the entire exercise table to show that the record has been added.
    """
    if request.method == "POST":
        try:
            query_db(
                "INSERT INTO student (txt_student_name, fk_section_id, ts_time_recorded) VALUES (?, ?, ?);",
                (
                    request.json["student_name"],
                    request.json["section_id"],
                    time.mktime(datetime.now().timetuple()),
                ),
            )
        except Exception as e:
            return f"An error occurred.\n{e}"

        return list(dict(row) for row in query_db("SELECT * FROM student;"))

    elif request.method == "GET":
        try:
            return list(
                dict(row)
                for row in query_db(
                    "SELECT * FROM student WHERE fk_section_id = ? AND txt_student_name LIKE ? AND ts_time_recorded BETWEEN ? AND ?;",
                    (
                        request.json["section_id"],
                        f'%{request.json["student_name"]}%',
                        request.json["timestamp_min"],
                        request.json["timestamp_max"],
                    ),
                )
            )
        except Exception as e:
            return f"An error occurred.\n{e}"


@app.route("/api/exercise}")
def api_exercise():
    """Handle GET and POST requests made to /api/exercise.
    On a GET request, returns an array of dictionaries which represent the results of the query made
    On a POST request, adds the designated exercise to the database and returns the entire exercise table to show that the record has been added.
    """
    if request.method == "POST":
        try:
            query_db(
                "INSERT INTO exercise (fk_section_id, txt_starting_code, txt_desired_output, ts_time_recorded) VALUES (?, ?, ?, ?);",
                (
                    request.json["section_id"],
                    request.json["starting_code"],
                    request.json["desired_output"],
                    time.mktime(datetime.now().timetuple()),
                ),
            )
        except Exception as e:
            return f"An error occurred.\n{e}"

        return list(dict(row) for row in query_db("SELECT * FROM exercise;"))

    elif request.method == "GET":
        try:
            return list(
                dict(row)
                for row in query_db(
                    "SELECT * FROM exercise WHERE fk_section_id = ? AND txt_starting_code LIKE ? AND txt_desired_output LIKE ? AND ts_time_recorded BETWEEN ? AND ?;",
                    (
                        request.json["section_id"],
                        f'%{request.json["starting_code"]}%',
                        f'%{request.json["desired_output"]}%',
                        request.json["timestamp_min"],
                        request.json["timestamp_max"],
                    ),
                )
            )
        except Exception as e:
            return f"An error occurred.\n{e}"


@app.route("/api/section", methods=["GET", "POST"])
def api_section():
    """Handle GET and POST requests made to /api/section.
    On a GET request, returns an array of dictionaries which represent the results of the query made
    On a POST request, adds the designated section to the database and returns the entire section table to show that the record has been added.
    """
    if request.method == "POST":
        try:
            query_db(
                "INSERT INTO section (txt_section_name, txt_instructor_name, ts_time_recorded) VALUES (?, ?, ?);",
                (
                    request.json["section_name"],
                    request.json["instructor_name"],
                    time.mktime(datetime.now().timetuple()),
                ),
            )
        except Exception as e:
            return f"An error occurred.\n{e}"

        return list(dict(row) for row in query_db("SELECT * FROM section;"))

    elif request.method == "GET":
        try:
            return list(
                dict(row)
                for row in query_db(
                    "SELECT * FROM section WHERE txt_section_name LIKE ? AND txt_instructor_name LIKE ? AND ts_time_recorded BETWEEN ? AND ?;",
                    (
                        f'%{request.json["section_name"]}%',
                        f'%{request.json["instructor_name"]}%',
                        request.json["timestamp_min"],
                        request.json["timestamp_max"],
                    ),
                )
            )
        except Exception as e:
            return f"An error occurred.\n{e}"


@app.route("/api/submission}", methods=["GET", "POST"])
def api_submission():
    """Handle GET and POST requests made to /api/section.
    On a GET request, returns an array of dictionaries which represent the results of the query made
    On a POST request, adds the designated section to the database and returns the entire section table to show that the record has been added.
    """
    if request.method == "POST":
        try:
            query_db(
                "INSERT INTO student_submission (txt_student_program, txt_student_program_output, bool_is_complete, ts_starting_time, ts_submission_time, fk_exercise_id, fk_student_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                (
                    request.json["student_program"],
                    request.json["student_program_output"],
                    request.json["is_complete"],
                    request.json["starting_time"],
                    request.json["submission_time"],
                    time.mktime(datetime.now().timetuple()),
                    request.json["exercise_id"],
                    request.json["student_id"],
                ),
            )
        except Exception as e:
            return f"An error occurred.\n{e}"

        return list(dict(row) for row in query_db("SELECT * FROM student_submission;"))

    elif request.method == "GET":
        try:
            return list(
                dict(row)
                for row in query_db(
                    """
                        SELECT * 
                        FROM student_submission 
                        WHERE 
                            txt_student_program LIKE ? 
                            AND txt_student_program_output LIKE ? 
                            AND bool_is_complete = ? 
                            AND ts_starting_time BETWEEN ? AND ?
                            AND ts_submission_time BETWEEN ? AND ?
                            AND ts_time_recorded BETWEEN ? AND ?
                            AND fk_exercise_id = ?
                            AND fk_student_id = ?;
                    """,
                    (
                        f'%{request.json["student_program"]}%',
                        f'%{request.json["student_program_output"]}%',
                        request.json["is_complete"],
                        request.json["starting_time_min"],
                        request.json["starting_time_max"],
                        request.json["submission_time_min"],
                        request.json["submission_time_max"],
                        request.json["time_recorded_min"],
                        request.json["time_recorded_max"],
                        request.json["exercise_id"],
                        request.json["student_id"],
                    ),
                )
            )
        except Exception as e:
            return f"An error occurred.\n{e}"
