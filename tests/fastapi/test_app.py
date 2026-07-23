from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity_adds_participant():
    email = "test_student@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup?email=test_student%40mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400():
    email = "duplicate_student@mergington.edu"

    first_response = client.post(
        "/activities/Chess%20Club/signup?email=duplicate_student%40mergington.edu"
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/activities/Chess%20Club/signup?email=duplicate_student%40mergington.edu"
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_removes_existing_participant():
    email = "removable_student@mergington.edu"

    signup_response = client.post(
        "/activities/Chess%20Club/signup?email=removable_student%40mergington.edu"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        "/activities/Chess%20Club/participants?email=removable_student%40mergington.edu"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_404():
    response = client.delete(
        "/activities/Chess%20Club/participants?email=not_registered%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
