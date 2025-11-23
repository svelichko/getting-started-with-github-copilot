import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for key in activities:
        assert key in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure user is not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404


def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister?email=foo@bar.com")
    assert response.status_code == 404
