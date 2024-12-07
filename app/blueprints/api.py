""" Blueprint for handling user requests against the database """

import sqlite3
import os.path

from flask import Blueprint, g, request, current_app

api = Blueprint(
    "api",
    __name__,
)


def get_db():
    """
    Establishes a connection to the database. Requires an app context to run.
    See https://flask.palletsprojects.com/en/stable/patterns/sqlite3/ for more details.
    """
    db = getattr(g, "_database", None)
    if db is None:
        if os.path.isfile(current_app.config["DATABASE_PATH"]):
            print(current_app.config["DATABASE_PATH"])
            # If the database file exists, load it. Otherwise, init the database.
            db = g._database = sqlite3.connect(current_app.config["DATABASE_PATH"])
        else:
            # Regenerate database
            db = g._database = sqlite3.connect(current_app.config["DATABASE_PATH"])
            with current_app.open_resource("db/schema.sql") as f:
                db.cursor().executescript(f.read().decode("utf-8"))

            # If we are testing load test data
            if current_app.config["TESTING"]:
                with current_app.open_resource("db/load_testing_data.sql") as f:
                    db.cursor().executescript(f.read().decode("utf-8"))
            db.commit()

    db.row_factory = sqlite3.Row
    return db


def query_db(statement, args=(), one=False):
    """Executes a SQL statement against the database and returns the results."""
    cur = get_db().execute(statement, args)
    results = cur.fetchall()
    cur.close()

    return (results[0] if results else None) if one else results


@api.route("/student_start", methods=["POST"])
def api_post_student_start():
    """
    Create a new attempts object to show that a student began working on an exercise
    Finds or creates new rows in the exercise, section, and student tables.
    """

    try:
        query_db(
            """INSERT INTO attempts (exercise, section, student)
               VALUES (:exercise, :section, :student)""",
            request.json,
        )
    except sqlite3.OperationalError as db_error:
        print(db_error)
        return {
            "error": "A database error occurred. Please try again later. "
            + str(db_error)
        }, 500
    except KeyError:
        return {"error: bad request"}, 400

    return {"error": None}


@api.route("/student_end", methods=["POST"])
def api_post_student_end():
    """
    Updates a previous student submission record with information to
    show that the recorded student has finished the recorded exercise
    """

    try:
        query_db(
            """UPDATE attempts
               SET is_complete = 1,
                   submission_time = strftime('%s', 'now')
               WHERE
                 exercise = :exercise
                 and section = :section
                 and student = :student""",
            request.json,
        )
    except sqlite3.OperationalError as e:
        print(e)
        return {"error": "A database error occurred. Please try again later. "}, 500

    return {"error": None}


@api.route("/stats/<section>/<exercise>", methods=["GET"])
def api_get_stats(section, exercise):  # pylint: disable=unused-argument
    """
    Returns the number of students who have attempted a specific exercise
    and the number of students who have completed the exercise
    """
    try:
        return dict(
            query_db(
                """SELECT
                     COUNT(1) total_submissions,
                     SUM(is_complete) completed_submissions
                   FROM attempts
                   WHERE section = :section and exercise = :exercise""",
                locals(),
                one=True,
            )
        )
    except sqlite3.OperationalError as e:
        print(e)
        return {"error": "A database error occurred. Please try again later. "}, 500
