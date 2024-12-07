"""
Tests for the application's database API

Only tests the program's backend API, not the front-end. 
"""

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
        "api/markers",
        json={"name": "start", "exercise": "ex1", "section": "sec1", "student": "Mike"},
    )
    assert not "error" in response.json


def test_post_student_end(client):
    """Test the api/student_end endpoint"""
    # pylint: disable=redefined-outer-name
    response = client.post(
        "api/markers",
        json={"name": "complete", "exercise": "e", "section": "s", "student": "Bob"},
    )
    assert not "error" in response.json


def test_get_stats(client):
    """Test the api/stats endpoint"""
    # pylint: disable=redefined-outer-name
    response = client.get("api/markers?exercise=ex&section=sec")

    assert response.json["results"][0]["started"] == 5
    assert response.json["results"][0]["completed"] == 3
