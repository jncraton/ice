"""
Tests for the application's database API

Only tests the program's backend API, not the front-end. 
"""

import time
import json
from datetime import datetime

import pytest

from app import create_app


@pytest.fixture()
def client():
    """ Define client fixture for use in tests """
    yield create_app(True).test_client()


def test_post_student_start(client):
    """Test the api/student_start endpoint"""
    # pylint: disable=redefined-outer-name
    initial_time = time.mktime(datetime.now().timetuple())
    response = client.post(
        "api/student_start",
        data=json.dumps(
            {
                "student_name": "Mike",
                "exercise_starting_code": "for i in range(5):",
                "exercise_desired_output": "1 2 3 4 5",
                "section_name": "CPSC 2020",
                "instructor_name": "Jon Craton",
                "exercise_name": "Intro to For Loops",
            }
        ),
        mimetype="application/json",
    )

    assert (
        initial_time
        <= response.json["time_started"]
        <= time.mktime(datetime.now().timetuple())
    )


def test_post_student_end(client):
    """Test the api/student_end endpoint"""
    # pylint: disable=redefined-outer-name
    end_time = time.mktime(datetime.now().timetuple())
    response = client.post(
        "api/student_end",
        data=json.dumps(
            {
                "student_name": "David",
                "student_final_code": "for i in range(5):\n\tprint(i)",
                "exercise_name": "Intro To For Loops",
                "exercise_starting_code": "for i in range(5):",
                "exercise_desired_output": "0 1 2 3 4",
                "section_name": "CPSC 2020",
                "instructor_name": "Jon Craton",
            }
        ),
        mimetype="application/json",
    )
    print(response.data)
    assert (
        end_time
        <= response.json["time_finished"]
        <= time.mktime(datetime.now().timetuple())
    )


def test_get_stats(client):
    """Test the api/stats endpoint"""
    # pylint: disable=redefined-outer-name
    response = client.get(
        "api/stats/Jon Craton/CPSC 2020/Intro To For Loops",
    )

    assert response.json["total_submissions"] == 5
    assert response.json["completed_submissions"] == 3
    assert response.json["incomplete_submissions"] == 2
