""" Blueprint for handling user requests against the database """

from datetime import datetime
import time
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
    Create a new student_submission object to show that a student began working on an exercise
    Finds or creates new rows in the exercise, section, and student tables.
    """
    print("---POST START---")
    # 1. Get time to log (do this first to maintain accuracy in timing!)
    starting_time = time.mktime(datetime.now().timetuple())

    try:
        print("Find/Create section")
        # 1. Find or Create Section
        # 1A. Query for section
        section_query = query_db(
            """
            SELECT section_id 
            FROM section 
            WHERE section_name = :section_name
                AND instructor_name = :instructor_name;
            """,
            request.json,
            one=True,
        )
        if section_query is not None:
            section_id = dict(section_query)["section_id"]
        else:
            # 1B. Create section if needed
            query_db(
                """
                INSERT INTO section 
                (
                    section_name, 
                    instructor_name, 
                )
                VALUES 
                (
                    :section_name, 
                    :instructor_name, 
                );
                """,
                request.json,
            )

            section_id = query_db(
                "SELECT last_insert_rowid() rowid;",
                one=True,
            )["rowid"]

        # 2. Find or Create Exercise
        print("Find/create exercise")
        # 2A. Query for exercise
        exercise_query = query_db(
            """
            SELECT exercise_id 
            FROM exercise 
            WHERE exercise_name = :exercise_name
                AND starting_code = :exercise_starting_code
                AND desired_output = :exercise_desired_output 
                AND section_id = :section_id;
            """,
            {**request.json, **{"section_id": section_id}},
            one=True,
        )
        if exercise_query is not None:
            print("Exercise found ")
            exercise_id = exercise_query["exercise_id"]
        else:
            print("Exercise needs recorded")
            # 2B. Create exercise if needed
            query_db(
                """
                INSERT INTO exercise 
                (
                    exercise_name, 
                    starting_code, 
                    desired_output, 
                    section_id
                ) 
                VALUES 
                (
                    :exercise_name,
                    :exercise_starting_code,
                    :exercise_desired_output,
                    :section_id
                );
                """, {**request.json, **locals()}
            )

            exercise_id = query_db(
                "SELECT last_insert_rowid() rowid;",
                one=True,
            )["rowid"]

        # 3. Find or Create Student
        print("Find/create Student")
        # 3A. Query for student
        student_query = query_db(
            """
            SELECT student_id 
            FROM student 
            WHERE student_name = :student_name
                AND section_id = :section_id;
            """, {**request.json, **locals()},
            one=True,
        )
        if student_query is not None:
            student_id = student_query["student_id"]
        else:
            # 3B. Create student if needed
            query_db(
                """
                INSERT INTO student 
                (
                    student_name, 
                    section_id
                ) 
                VALUES 
                (
                    :student_name, 
                    :section_id
                );
                """, {**request.json, **locals()}
            )

            student_id = query_db(
                "SELECT last_insert_rowid() rowid;",
                one=True,
            )["rowid"]

        # 4. Create Student Submission Object (but only if there isn't already one)
        print("Find/create student submission object")

        submission_query = query_db(
            """SELECT 
                    student_submission_id, 
                    starting_time 
                FROM student_submission 
                WHERE student_id = :student_id
                    AND exercise_id = :exercise_id
                    AND is_complete = 0;""",
            locals(),
            one=True,
        )

        if submission_query is not None:
            return {"time_started": submission_query["starting_time"]}

        print("Creating student submission object")
        print(len(list(dict(d) for d in query_db("SELECT * FROM student_submission;"))))
        query_db(
            """
            INSERT INTO student_submission 
            (
                starting_time, 
                exercise_id, 
                student_id
            ) 
            VALUES 
            (
                :starting_time, 
                :exercise_id, 
                :student_id
            );
            """, locals())
    except sqlite3.OperationalError as db_error:
        print(db_error)
        return {"error": "A database error occurred. Please try again later. "}, 500
    except KeyError:
        return {"error: bad request"}, 400

    # 5. Return confirmation that student submission object was created with time
    return {"time_started": starting_time}


@api.route("/student_end", methods=["POST"])
def api_post_student_end():
    """
    Updates a previous student submission record with information to
    show that the recorded student has finished the recorded exercise
    """
    time_ended = time.mktime(datetime.now().timetuple())
    print(len(list(dict(d) for d in query_db("SELECT * FROM student_submission;"))))
    # 1. Select the right query
    query = query_db(
        """SELECT student_submission_id FROM student_submission st_s
            INNER JOIN exercise e 
                ON e.exercise_id = st_s.exercise_id
            INNER JOIN section s
                ON s.section_id = e.section_id 
            INNER JOIN student st 
                ON st.student_id = st_s.student_id
            WHERE 
                s.section_name = :section_name
            AND s.instructor_name = :instructor_name
            AND e.exercise_name = :exercise_name
            AND st.student_name = :student_name
            AND e.starting_code = :exercise_starting_code
            AND e.desired_output = :exercise_desired_output
            AND st_s.is_complete = 0;
            """,
        request.json,
        one=True,
    )

    if query is None:
        print("Can't find it")
        print("404 error")
        return {"error": "no previous submission started"}, 404
    query_db(
        """UPDATE student_submission
            SET student_program = :student_program,
                student_program_output = :student_program_output,
                is_complete = :is_complete,
                submission_time = :submission_time
            WHERE 
                student_submission_id = :student_submission_id;
        """,
        {
            "student_program": request.json["student_final_code"],
            "student_program_output": request.json["exercise_desired_output"],
            "is_complete": 1,
            "submission_time": time_ended,
            "student_submission_id": query["student_submission_id"],
        },
    )

    return {"time_finished": time_ended}


@api.route("/stats/<instructor_name>/<section_name>/<exercise_name>", methods=["GET"])
def api_get_stats(
    instructor_name, section_name, exercise_name
):  # pylint: disable=unused-argument
    """
    Returns the number of students who have attempted a specific exercise,
    the number of students who have completed the exercise, and the number
    of students who have not completed the exercise.
    """
    try:
        return dict(
            query_db(
                """
                SELECT
                    COUNT(st_s.student_submission_id) total_submissions,
                    SUM(is_complete) completed_submissions,
                    (
                        COUNT(st_s.student_submission_id) - SUM(is_complete)
                    ) incomplete_submissions
                FROM student_submission st_s
                INNER JOIN exercise e 
                    ON e.exercise_id = st_s.exercise_id
                INNER JOIN section s
                    ON s.section_id = e.section_id 
                WHERE 
                    s.section_name = :section_name
                AND s.instructor_name = :instructor_name
                AND e.exercise_name = :exercise_name;
                """,
                locals(),
                one=True,
            )
        )
    except sqlite3.OperationalError as e:
        print(e)
        return {"error": "A database error occurred. Please try again later. "}, 500
