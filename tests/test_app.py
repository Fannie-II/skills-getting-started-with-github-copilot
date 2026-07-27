from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_adds_participant():
    activity_name = "Chess Club"
    email = "newstudent@example.com"

    activities[activity_name]["participants"] = []

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "existing@example.com"

    activities[activity_name]["participants"] = [email]

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_their_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    activities[activity_name]["participants"] = [email, "daniel@mergington.edu"]

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert activities[activity_name]["participants"] == ["daniel@mergington.edu"]
