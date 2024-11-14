"""
Tests for the application's database API

Only tests the program's backend API, not the front-end. 
"""

import pytest
import json
from app.app import create_app


@pytest.fixture
def client():
    # app.config["TESTING"] = True
    yield create_app(True).test_client()


def test_database_api(client):
    response = client.post(
        "/api/section",
        data=json.dumps(
            {
                "txt_section_name": "Intro to Computer Science",
                "txt_instructor_name": "Professor Smith",
            }
        ),
        mimetype="application/json",
    )

    assert len(response.json) == 1
    assert response.json[0]["txt_section_name"] == "Intro to Computer Science"
    assert response.json[0]["txt_instructor_name"] == "Professor Smith"
