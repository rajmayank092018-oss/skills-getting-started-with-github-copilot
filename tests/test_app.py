import os
import sys

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity keys
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    test_email = "testuser@example.com"

    # Ensure test_email not present initially
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    if test_email in participants:
        # Remove if leftover from previous run
        client.delete(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert test_email in client.get("/activities").json()[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert resp.status_code == 200
    assert test_email not in client.get("/activities").json()[activity]["participants"]
