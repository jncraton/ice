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
    time_started = time.mktime(datetime.now().timetuple())

    try:
        print("Find/Create section")
        # 1. Find or Create Section
        # 1A. Query for section
        section_query = query_db(
            """
            SELECT pk_section_id 
            FROM section 
            WHERE txt_section_name = :section_name
                AND txt_instructor_name = :instructor_name;
            """,
            {
                "section_name": request.json["section_name"],
                "instructor_name": request.json["instructor_name"],
            },
            one=True,
        )
        if section_query is not None:
            section_id = dict(section_query)["pk_section_id"]
        else:
            # 1B. Create section if needed
            query_db(
                """
                INSERT INTO section 
                (
                    txt_section_name, 
                    txt_instructor_name, 
                    ts_time_recorded
                )
                VALUES 
                (
                    :section_name, 
                    :instructor_name, 
                    :time_recorded
                );
                """,
                {
                    "section_name": request.json["section_name"],
                    "instructor_name": request.json["instructor_name"],
                    "time_recorded": time.mktime(datetime.now().timetuple()),
                },
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
            SELECT pk_exercise_id 
            FROM exercise 
            WHERE txt_exercise_name = :exercise_name
                AND txt_starting_code = :exercise_starting_code
                AND txt_desired_output = :exercise_desired_output 
                AND fk_section_id = :section_id;
            """,
            {
                "exercise_name": request.json["exercise_name"],
                "exercise_starting_code": request.json["exercise_starting_code"],
                "exercise_desired_output": request.json["exercise_desired_output"],
                "section_id": section_id,
            },
            one=True,
        )
        if exercise_query is not None:
            print("Exercise found ")
            exercise_id = exercise_query["pk_exercise_id"]
        else:
            print("Exercise needs recorded")
            # 2B. Create exercise if needed
            query_db(
                """
                INSERT INTO exercise 
                (
                    txt_exercise_name, 
                    txt_starting_code, 
                    txt_desired_output, 
                    fk_section_id, 
                    ts_time_recorded
                ) 
                VALUES 
                (
                    :exercise_name,
                    :exercise_starting_code,
                    :exercise_desired_output,
                    :section_id,
                    :time_recorded
                );
                """,
                {
                    "exercise_name": request.json["exercise_name"],
                    "exercise_starting_code": request.json["exercise_starting_code"],
                    "exercise_desired_output": request.json["exercise_desired_output"],
                    "section_id": section_id,
                    "time_recorded": time.mktime(datetime.now().timetuple()),
                },
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
            SELECT pk_student_id 
            FROM student 
            WHERE txt_student_name = :student_name
                AND fk_section_id = :section_id;
            """,
            {
                "student_name": request.json["student_name"],
                "section_id": section_id,
            },
            one=True,
        )
        if student_query is not None:
            student_id = student_query["pk_student_id"]
        else:
            # 3B. Create student if needed
            query_db(
                """
                INSERT INTO student 
                (
                    txt_student_name, 
                    fk_section_id, 
                    ts_time_recorded
                ) 
                VALUES 
                (
                    :student_name, 
                    :section_id, 
                    :time_recorded
                );
                """,
                {
                    "student_name": request.json["student_name"],
                    "section_id": section_id,
                    "time_recorded": time.mktime(datetime.now().timetuple()),
                },
            )

            student_id = query_db(
                "SELECT last_insert_rowid() rowid;",
                one=True,
            )["rowid"]

        # 4. Create Student Submission Object (but only if there isn't already one)
        print("Find/create student submission object")

        submission_query = query_db(
            """SELECT 
                    pk_student_submission_id, 
                    ts_starting_time 
                FROM student_submission 
                WHERE fk_student_id = :student_id
                    AND fk_exercise_id = :exercise_id
                    AND bool_is_complete = FALSE;""",
            {"student_id": student_id, "exercise_id": exercise_id},
            one=True,
        )

        if submission_query is not None:
            return {"time_started": submission_query["ts_starting_time"]}

        print("Creating student submission object")
        print(len(list(dict(d) for d in query_db("SELECT * FROM student_submission;"))))
        query_db(
            """
            INSERT INTO student_submission 
            (
                txt_student_program, 
                txt_student_program_output, 
                bool_is_complete, 
                ts_starting_time, 
                ts_submission_time, 
                ts_time_recorded, 
                fk_exercise_id, 
                fk_student_id
            ) 
            VALUES 
            (
                :txt_student_program, 
                :txt_student_program_output, 
                :bool_is_complete, 
                :ts_starting_time, 
                :ts_submission_time, 
                :ts_time_recorded, 
                :fk_exercise_id, 
                :fk_student_id
            );
            """,
            {
                "txt_student_program": "",
                "txt_student_program_output": "",
                "bool_is_complete": False,
                "ts_starting_time": time_started,
                "ts_submission_time": None,
                "ts_time_recorded":time.mktime(datetime.now().timetuple()),
                "fk_exercise_id": exercise_id,
                "fk_student_id": student_id
            },
        )
    except sqlite3.OperationalError as db_error:
        print(db_error)
        return {"error": "A database error occurred. Please try again later. "}, 500
    except KeyError:
        return {"error: bad request"}, 400

    # 5. Return confirmation that student submission object was created with time X
    return {"time_started": time_started}


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
        """SELECT pk_student_submission_id FROM student_submission st_s
            INNER JOIN exercise e 
                ON e.pk_exercise_id = st_s.fk_exercise_id
            INNER JOIN section s
                ON s.pk_section_id = e.fk_section_id 
            INNER JOIN student st 
                ON st.pk_student_id = st_s.fk_student_id
            WHERE 
                s.txt_section_name = :section_name
            AND s.txt_instructor_name = :instructor_name
            AND e.txt_exercise_name = :exercise_name
            AND st.txt_student_name = :student_name
            AND e.txt_starting_code = :exercise_starting_code
            AND e.txt_desired_output = :exercise_desired_output
            AND st_s.bool_is_complete = FALSE;
            """,
        {
            "section_name": request.json["section_name"],
            "instructor_name": request.json["instructor_name"],
            "exercise_name": request.json["exercise_name"],
            "student_name": request.json["student_name"],
            "exercise_starting_code": request.json["exercise_starting_code"],
            "exercise_desired_output": request.json["exercise_desired_output"],
        },
        one=True,
    )

    if query is None:
        print("Can't find it")
        print("404 error")
        return {"error": "no previous submission started"}, 404
    query_db(
        """UPDATE student_submission
            SET txt_student_program = :student_program,
                txt_student_program_output = :student_program_output,
                bool_is_complete = :is_complete,
                ts_submission_time = :submission_time,
                ts_time_recorded = :time_recorded
            WHERE 
                pk_student_submission_id = :student_submission_id;
        """,
        {
            "student_program": request.json["student_final_code"],
            "student_program_output": request.json["exercise_desired_output"],
            "is_complete": True,
            "submission_time": time_ended,
            "time_recorded": time.mktime(datetime.now().timetuple()),
            "student_submission_id": query["pk_student_submission_id"],
        },
    )

    return {"time_finished": time_ended}


@api.route("/stats/<instructor_name>/<section_name>/<exercise_name>", methods=["GET"])
def api_get_stats(instructor_name, section_name, exercise_name):
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
                    COUNT(st_s.pk_student_submission_id) total_submissions,
                    SUM(bool_is_complete) completed_submissions,
                    (
                        COUNT(st_s.pk_student_submission_id) - SUM(bool_is_complete)
                    ) incomplete_submissions
                FROM student_submission st_s
                INNER JOIN exercise e 
                    ON e.pk_exercise_id = st_s.fk_exercise_id
                INNER JOIN section s
                    ON s.pk_section_id = e.fk_section_id 
                WHERE 
                    s.txt_section_name = :section_name
                AND s.txt_instructor_name = :instructor_name
                AND e.txt_exercise_name = :exercise_name;
                """,
                {
                    "section_name": section_name,
                    "instructor_name": instructor_name,
                    "exercise_name": exercise_name,
                },
                one=True,
            )
        )
    except sqlite3.OperationalError as e:
        print(e)
        return {"error": "A database error occurred. Please try again later. "}, 500
