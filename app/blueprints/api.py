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

    return {"results": [dict(r) for r in results]}

@api.route("/markers", methods=["POST"])
def post_marker():
    """Creates a new marker to track student progress on an exercise"""

    return query_db(
        """INSERT OR IGNORE INTO markers (exercise, section, student, name)
           VALUES (:exercise, :section, :student, :name)""",
        request.json
    )


@api.route("/markers", methods=["GET"])
def get_markers():
    """Returns exercise stats"""

    return query_db(
        """SELECT SUM(name = 'start') started, SUM(name = 'complete') completed
           FROM markers
           WHERE section = :section and exercise = :exercise""",
        request.args,
        one=True,
    )
