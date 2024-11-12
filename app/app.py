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
                db.cursor().executescript(f.read())
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
def add_student():
    # return query_db("INSERT INTO student ()")
    pass


@app.route("/api/activity}")
def add_activity():
    pass


@app.route("/api/section", methods=["GET", "POST"])
def add_section():
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
                    "SELECT * FROM section WHERE txt_section_name = ? AND txt_instructor_name = ? AND ts_time_recorded BETWEEN ? AND ?;",
                    (
                        request.json["section_name"],
                        request.json["instructor_name"],
                        request.json["timestamp_min"],
                        request.json["timestamp_max"],
                    ),
                )
            )
        except Exception as e:
            return f"An error occurred.\n{e}"


@app.route("/api/submission}", methods=["GET", "POST"])
def add_submission():
    pass
