from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball" in data


def test_signup_and_unregister():
    activity = "Basketball"
    email = "test_signup@example.com"

    # Ensure clean start
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate sign up should fail
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r2.status_code == 400

    # Unregister
    r3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r3.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should fail
    r4 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r4.status_code == 400


def test_signup_nonexistent_activity():
    r = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert r.status_code == 404


def test_unregister_nonexistent_activity():
    r = client.post("/activities/NoSuchActivity/unregister?email=a@b.com")
    assert r.status_code == 404
