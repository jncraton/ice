""" Blueprint for handling user requests against the database """

import sqlite3
import os.path

from flask import Blueprint, request, current_app

api = Blueprint("api", __name__)


def query_db(statement, args=(), one=False):
    """Executes a SQL statement against the database and returns the results."""

    if os.path.isfile(current_app.config["DATABASE_PATH"]):
        # If the database file exists, connect
        db = sqlite3.connect(current_app.config["DATABASE_PATH"])
    else:
        # Otherwise regenerate database
        db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        with current_app.open_resource("db/schema.sql") as f:
            db.executescript(f.read().decode("utf-8"))

        # If we are testing load test data
        if current_app.config["TESTING"]:
            with current_app.open_resource("db/load_testing_data.sql") as f:
                db.cursor().executescript(f.read().decode("utf-8"))

    db.row_factory = sqlite3.Row

    try:
        results = db.execute(statement, args).fetchall()
        db.commit()
        db.close()
    except sqlite3.OperationalError:
        return {"error": "Database error"}, 500
    except KeyError:
        return {"error": "Bad request"}, 400

    results = [dict(r) for r in results]

    return (results[0] if results else None) if one else results


@api.route("/student_start", methods=["POST"])
def api_post_student_start():
    """Creates a new attempt to show that a student began working on an exercise"""

    return query_db(
        """INSERT INTO attempts (exercise, section, student)
           VALUES (:exercise, :section, :student)""",
        request.json,
    )


@api.route("/student_end", methods=["POST"])
def api_post_student_end():
    """Updates attempt to log completion"""

    return query_db(
        """UPDATE attempts
           SET is_complete = 1,
               submission_time = strftime('%s', 'now')
           WHERE
             exercise = :exercise
             and section = :section
             and student = :student""",
        request.json,
    )


@api.route("/stats/<section>/<exercise>", methods=["GET"])
def api_get_stats(section, exercise):  # pylint: disable=unused-argument
    """Returns exercise stats"""

    return query_db(
        """SELECT COUNT(1) started, SUM(is_complete) completed
           FROM attempts
           WHERE section = :section and exercise = :exercise""",
        locals(),
        one=True,
    )
