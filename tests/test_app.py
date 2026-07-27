from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_their_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    activities[activity_name]["participants"] = [email, "daniel@mergington.edu"]

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert activities[activity_name]["participants"] == ["daniel@mergington.edu"]
