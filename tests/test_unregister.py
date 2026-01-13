from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_unregister_participant_flow():
    email = "temp_user@example.com"

    # Ensure signup works
    resp_signup = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert resp_signup.status_code == 200
    assert "Signed up" in resp_signup.json()["message"]

    # Confirm participant appears in activities listing
    resp_acts = client.get("/activities")
    assert resp_acts.status_code == 200
    activities = resp_acts.json()
    assert email in activities["Chess Club"]["participants"]

    # Now unregister
    resp_unreg = client.delete("/activities/Chess%20Club/participants", params={"email": email})
    assert resp_unreg.status_code == 200
    assert "Unregistered" in resp_unreg.json()["message"]

    # Trying to unregister again should fail
    resp_unreg2 = client.delete("/activities/Chess%20Club/participants", params={"email": email})
    assert resp_unreg2.status_code == 400