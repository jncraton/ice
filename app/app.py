"""
    Flask server for running the API for the database and web server for the application. 

    Currently provides routes to all static files in the `www` directory
"""

import sqlite3
import os.path
from flask import Flask, request, g
from datetime import datetime
import time

from config import Config, TestConfig

# app = Flask(__name__, static_folder="../www")


def create_app(testing=False):
    app = Flask(__name__, static_folder="../www")

    if testing:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    # DATABASE_PATH = "../app/db/ice-database.db"

    # Set up database
    def get_db():
        """
        Establishes a connection to the database. Requires an app context to run.
        See https://flask.palletsprojects.com/en/stable/patterns/sqlite3/ for more details.
        """
        db = getattr(g, "_database", None)
        if db is None:
            if os.path.isfile(app.config["DATABASE_PATH"]):
                print(app.config["DATABASE_PATH"])
                # If the database file exists, load it. Otherwise, init the database.
                db = g._database = sqlite3.connect(app.config["DATABASE_PATH"])
            else:
                db = g._database = sqlite3.connect(app.config["DATABASE_PATH"])
                with app.open_resource("db/schema.sql") as f:
                    db.cursor().executescript(f.read().decode("utf-8"))

                if app.config["TESTING"]:
                    with app.open_resource("db/load_testing_data.sql") as f:
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
    @app.route("/api/student", methods=["GET", "POST"])
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
                        request.json["txt_student_name"],
                        request.json["fk_section_id"],
                        time.mktime(datetime.now().timetuple()),
                    ),
                )
            except Exception as e:
                return f"An error occurred.\n{e}"

            return dict(
                query_db(
                    "SELECT * FROM student WHERE pk_student_id = last_insert_rowid();",
                    one=True,
                )
            )

        elif request.method == "GET":

            if "pk_student_id" in request.json.keys():
                try:
                    return dict(
                        query_db(
                            "SELECT * FROM student WHERE pk_student_id = ?;",
                            (request.json["pk_student_id"],),
                            one=True,
                        )
                    )
                except TypeError as e:
                    return f'No student found with id {request.json["pk_student_id"]}'

            student_name = f'%{request.json["txt_student_name"] if "txt_student_name" in request.json.keys() else ""}%'

            time_recorded_min = (
                request.json["ts_time_recorded_min"]
                if "ts_time_recorded_min" in request.json.keys()
                else 0
            )
            time_recorded_max = (
                request.json["ts_time_recorded_max"]
                if "ts_time_recorded_max" in request.json.keys()
                else time.mktime(datetime.now().timetuple())
            )
            try:
                if "fk_section_id" in request.json.keys():
                    return list(
                        dict(row)
                        for row in query_db(
                            f"SELECT * FROM student WHERE fk_section_id = ? AND txt_student_name LIKE ? AND ts_time_recorded BETWEEN ? AND ?;",
                            (
                                request.json["fk_section_id"],
                                student_name,
                                time_recorded_min,
                                time_recorded_max,
                            ),
                        )
                    )
                else:
                    return list(
                        dict(row)
                        for row in query_db(
                            f"SELECT * FROM student WHERE txt_student_name LIKE ? AND ts_time_recorded BETWEEN ? AND ?;",
                            (student_name, time_recorded_min, time_recorded_max),
                        )
                    )

            except Exception as e:
                return f"An error occurred.\n{e}"

    @app.route("/api/exercise", methods=["GET", "POST"])
    def api_exercise():
        """Handle GET and POST requests made to /api/exercise.
        On a GET request, returns an array of dictionaries which represent the results of the query made
        On a POST request, adds the designated exercise to the database and returns the entire exercise table to show that the record has been added.
        """
        if request.method == "POST":
            try:
                query_db(
                    "INSERT INTO exercise (fk_section_id, txt_exercise_name, txt_starting_code, txt_desired_output, ts_time_recorded) VALUES (?, ?, ?, ?, ?);",
                    (
                        request.json["fk_section_id"],
                        request.json["txt_exercise_name"],
                        request.json["txt_starting_code"],
                        request.json["txt_desired_output"],
                        time.mktime(datetime.now().timetuple()),
                    ),
                )
            except Exception as e:
                return f"An error occurred.\n{e}"
            return dict(
                query_db(
                    "SELECT * FROM exercise WHERE pk_exercise_id = last_insert_rowid();",
                    one=True,
                )
            )

        elif request.method == "GET":
            try:
                if "pk_exercise_id" in request.json.keys():
                    return dict(
                        query_db(
                            "SELECT * FROM exercise WHERE pk_exercise_id = ?;",
                            (request.json["pk_exercise_id"],),
                            one=True,
                        )
                    )
            except TypeError as e:
                return f'No student found with id {request.json["pk_exercise_id"]}'

            try:
                exercise_name = f'%{request.json["txt_exercise_name"] if "txt_exercise_name" in request.json.keys() else ""}%'
                starting_code = f'%{request.json["txt_starting_code"] if "txt_starting_code" in request.json.keys() else ""}%'
                desired_output = f'%{request.json["txt_desired_output"] if "txt_desired_output" in request.json.keys() else ""}%'
                time_recorded_min = (
                    request.json["ts_time_recorded_min"]
                    if "ts_time_recorded_min" in request.json.keys()
                    else 0
                )
                time_recorded_max = (
                    request.json["ts_time_recorded_max"]
                    if "ts_time_recorded_max" in request.json.keys()
                    else time.mktime(datetime.now().timetuple())
                )
                if "fk_section_id" in request.json.keys():
                    return list(
                        dict(row)
                        for row in query_db(
                            "SELECT * FROM exercise WHERE fk_section_id = ? AND txt_exercise_name LIKE ? AND txt_starting_code LIKE ? AND txt_desired_output LIKE ? AND ts_time_recorded BETWEEN ? AND ?;",
                            (
                                request.json["fk_section_id"],
                                exercise_name,
                                starting_code,
                                desired_output,
                                time_recorded_min,
                                time_recorded_max,
                            ),
                        )
                    )
                else:
                    return list(
                        dict(row)
                        for row in query_db(
                            "SELECT * FROM exercise WHERE txt_exercise_name LIKE ? AND txt_starting_code LIKE ? AND txt_desired_output LIKE ? AND ts_time_recorded BETWEEN ? AND ?;",
                            (
                                exercise_name,
                                starting_code,
                                desired_output,
                                time_recorded_min,
                                time_recorded_max,
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
                    "INSERT INTO section (txt_section_name, ts_time_recorded) VALUES (?, ?);",
                    (
                        request.json["txt_section_name"],
                        time.mktime(datetime.now().timetuple()),
                    ),
                )
            except Exception as e:
                return f"An error occurred.\n{e}"

            return dict(
                query_db(
                    "SELECT * FROM section WHERE pk_section_id = last_insert_rowid()",
                    one=True,
                )
            )

        elif request.method == "GET":
            try:
                if "pk_section_id" in request.json.keys():
                    return dict(
                        query_db(
                            "SELECT * FROM section WHERE pk_section_id = ?;",
                            (request.json["pk_section_id"],),
                            one=True,
                        )
                    )
            except TypeError as e:
                return f'No student found with id {request.json["pk_section_id"]}'

            try:
                section_name = f'%{request.json["txt_section_name"] if "txt_section_name" in request.json.keys() else ""}%'
                time_recorded_min = (
                    request.json["ts_time_recorded_min"]
                    if "ts_time_recorded_min" in request.json.keys()
                    else 0
                )
                time_recorded_max = (
                    request.json["ts_time_recorded_max"]
                    if "ts_time_recorded_max" in request.json.keys()
                    else time.mktime(datetime.now().timetuple())
                )
                return list(
                    dict(row)
                    for row in query_db(
                        "SELECT * FROM section WHERE txt_section_name LIKE ? AND txt_instructor_name LIKE ? AND ts_time_recorded BETWEEN ? AND ?;",
                        (
                            section_name,
                            time_recorded_min,
                            time_recorded_max,
                        ),
                    )
                )
            except Exception as e:
                return f"An error occurred.\n{e}"

    @app.route("/api/submission", methods=["GET", "POST"])
    def api_submission():
        """Handle GET and POST requests made to /api/section.
        On a GET request, returns an array of dictionaries which represent the results of the query made
        On a POST request, adds the designated section to the database and returns the entire section table to show that the record has been added.
        """
        if request.method == "POST":
            try:
                query_db(
                    "INSERT INTO student_submission (txt_student_program, txt_student_program_output, bool_is_complete, ts_starting_time, ts_submission_time, ts_time_recorded, fk_exercise_id, fk_student_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                    (
                        request.json["txt_student_program"],
                        request.json["txt_student_program_output"],
                        request.json["bool_is_complete"],
                        request.json["ts_starting_time"],
                        request.json["ts_submission_time"],
                        time.mktime(datetime.now().timetuple()),
                        request.json["fk_exercise_id"],
                        request.json["fk_student_id"],
                    ),
                )
            except Exception as e:
                return f"An error occurred.\n{e}"

            return dict(
                query_db(
                    "SELECT * FROM student_submission WHERE pk_student_submission_id = last_insert_rowid();",
                    one=True,
                )
            )

        elif request.method == "GET":
            try:
                if "pk_student_submission_id" in request.json.keys():
                    return dict(
                        query_db(
                            "SELECT * FROM student_submission WHERE pk_student_submission_id = ?;",
                            (request.json["pk_student_submission_id"],),
                            one=True,
                        )
                    )
            except TypeError as e:
                return f'No student found with id {request.json["pk_student_submission_id"]}'

            try:
                student_program = f'%{request.json["txt_student_program"] if "txt_student_program" in request.json.keys() else ""}%'
                student_program_output = f'%{request.json["txt_student_program_output"] if "txt_student_program_output" in request.json.keys() else ""}%'
                # is_complete = request.json["bool_is_complete"] if "bool_is_complete" in request.json.keys else
                starting_time_min = (
                    request.json["ts_starting_time_min"]
                    if "ts_starting_time_min" in request.json.keys()
                    else 0
                )
                starting_time_max = (
                    request.json["ts_starting_time_max"]
                    if "ts_starting_time_max" in request.json.keys()
                    else time.mktime(datetime.now().timetuple())
                )
                submission_time_min = (
                    request.json["ts_submission_time_min"]
                    if "ts_submission_time_min" in request.json.keys()
                    else 0
                )
                submission_time_max = (
                    request.json["ts_submission_time_max"]
                    if "ts_submission_time_max" in request.json.keys()
                    else time.mktime(datetime.now().timetuple())
                )
                time_recorded_min = (
                    request.json["ts_time_recorded_min"]
                    if "ts_time_recorded_min" in request.json.keys()
                    else 0
                )
                time_recorded_max = (
                    request.json["ts_time_recorded_max"]
                    if "ts_time_recorded_max" in request.json.keys()
                    else time.mktime(datetime.now().timetuple())
                )

                sql = f"""
                    SELECT * 
                    FROM student_submission 
                    WHERE 
                        txt_student_program LIKE ? 
                        AND txt_student_program_output LIKE ? 
                        AND ts_starting_time BETWEEN ? AND ?
                        AND ts_submission_time BETWEEN ? AND ? 
                        AND ts_time_recorded BETWEEN ? AND ? 
                        {"AND bool_is_complete = ?" if "bool_is_complete" in request.json.keys() else ""}
                        {"AND fk_exercise_id = ?" if "fk_exercise_id" in request.json.keys() else ""}
                        {"AND fk_student_id = ?" if "fk_student_id" in request.json.keys() else ""}
                    ;
                """
                args = (
                    student_program,
                    student_program_output,
                    starting_time_min,
                    starting_time_max,
                    submission_time_min,
                    submission_time_max,
                    time_recorded_min,
                    time_recorded_max,
                )
                if "bool_is_complete" in request.json.keys():
                    args = args + (request.json["bool_is_complete"],)
                if "fk_exercise_id" in request.json.keys():
                    args = args + (request.json["fk_exercise_id"],)
                if "fk_student_id" in request.json.keys():
                    args = args + (request.json["fk_student_id"],)

                rows = query_db(sql, args)

                return list(dict(row) for row in rows)

            except Exception as e:
                return f"An error occurred.\n{e}"

    return app
