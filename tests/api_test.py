"""
Tests for the application's database API

Only tests the program's backend API, not the front-end. 
"""

import json

import pytest

from app import create_app


@pytest.fixture()
def client():
    """Define client fixture for use in tests"""
    yield create_app(True).test_client()


def test_post_student_start(client):
    """Test the api/student_start endpoint"""
    # pylint: disable=redefined-outer-name
    response = client.post(
        "api/student_start",
        data=json.dumps(
            {
                "student": "Mike",
                "section": "CPSC 2020",
                "exercise": "Intro to For Loops",
            }
        ),
        mimetype="application/json",
    )

    assert not response.json["error"]


def test_post_student_end(client):
    """Test the api/student_end endpoint"""
    # pylint: disable=redefined-outer-name
    response = client.post(
        "api/student_end",
        data=json.dumps(
            {
                "student": "David",
                "exercise": "Intro To For Loops",
                "section": "CPSC 2020",
            }
        ),
        mimetype="application/json",
    )
    assert not response.json["error"]


def test_get_stats(client):
    """Test the api/stats endpoint"""
    # pylint: disable=redefined-outer-name
    response = client.get(
        "api/stats/sec/ex",
    )

    assert response.json["started"] == 5
    assert response.json["completed"] == 3
