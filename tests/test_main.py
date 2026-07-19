"""Tests for API endpoints for the VoteTrackerPlus backend"""

from fastapi.testclient import TestClient

from vtp.web.api.main import app

client = TestClient(app)


def test_get_root():
    """Test the version endpoint"""
    response = client.get("/web-api/version")
    assert response.status_code == 200
    assert "version" in response.json()


# Endpoint #3
def test_cast_ballot(cast_ballot_response):
    """Test cast_ballot"""
    assert cast_ballot_response.status_code == 200
    data = cast_ballot_response.json()
    assert "vote_store_id" in data
    assert "ballot_check" in data
    assert "ballot_row" in data
    assert "encoded_qr" in data


# Endpoint #4
def test_verify_ballot_receipt(vote_store_id, ballot_receipt):
    """Testing the verification of a ballot receipt"""
    response = client.request(
        "GET",
        f"/web-api/verify_ballot_receipt/{vote_store_id}",
        json=ballot_receipt,
    )
    assert response.status_code == 200
    assert "verify_ballot_stdout" in response.json()


# Endpoint #5
def test_tally_election(vote_store_id):
    """Testing the tally"""
    response = client.get(f"/web-api/tally_contests/{vote_store_id}/None/None/3")
    assert response.status_code == 200
    assert "tally_election_stdout" in response.json()
