from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"]


def test_signup_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@example.com"

    activities[activity_name]["participants"] = []

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected(client):
    activity_name = "Chess Club"
    email = "existing@example.com"

    activities[activity_name]["participants"] = [email]

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_their_email(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    activities[activity_name]["participants"] = [email, "daniel@mergington.edu"]

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert activities[activity_name]["participants"] == ["daniel@mergington.edu"]
