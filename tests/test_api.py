from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location") == "/static/index.html"


def test_get_activities_structure():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]


def test_signup_and_unregister_flow():
    email = "test_flow@example.com"

    # Ensure the email is not present initially (cleanup if needed)
    resp_init = client.get("/activities")
    if email in resp_init.json()["Chess Club"]["participants"]:
        client.delete("/activities/Chess%20Club/participants", params={"email": email})

    # Signup
    r = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Duplicate signup should fail
    r2 = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert r2.status_code == 400

    # Confirm participant appears in activities
    acts = client.get("/activities").json()
    assert email in acts["Chess Club"]["participants"]

    # Unregister
    r3 = client.delete("/activities/Chess%20Club/participants", params={"email": email})
    assert r3.status_code == 200

    # Confirm removed
    acts2 = client.get("/activities").json()
    assert email not in acts2["Chess Club"]["participants"]

    # Unregistering again should fail
    r4 = client.delete("/activities/Chess%20Club/participants", params={"email": email})
    assert r4.status_code == 400


def test_signup_invalid_activity():
    r = client.post("/activities/NoSuchActivity/signup", params={"email": "noone@example.com"})
    assert r.status_code == 404
