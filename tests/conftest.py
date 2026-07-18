"""Shared pytest fixtures for VTP-web-api tests"""
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from vtp.web.api.main import App
from vtp.web.api.backend import VtpBackend

MOCK_DATA_DIR = Path(__file__).parent.parent / "src" / "vtp" / "web" / "api" / "mock-data"


@pytest.fixture(autouse=True)
def mock_mode(monkeypatch):
    """Force VtpBackend into mock mode for all tests in this session"""
    monkeypatch.setattr(VtpBackend, "_MOCK_MODE", True)


@pytest.fixture
def client():
    """A TestClient wrapping the FastAPI App"""
    return TestClient(App)


@pytest.fixture
def incoming_ballot_data():
    """A filled-in ballot, as the frontend would submit it"""
    with open(MOCK_DATA_DIR / "cast-ballot.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def blank_ballot_data():
    """An empty ballot template"""
    with open(MOCK_DATA_DIR / "blank-ballot.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def cast_ballot_response(client, incoming_ballot_data):
    """POST the mock ballot; runs against VtpBackend in mock mode"""
    return client.post("/web-api/cast_ballot", json=incoming_ballot_data)


@pytest.fixture
def vote_store_id(cast_ballot_response):
    """A vote_store_id from a (mocked) cast ballot response"""
    return cast_ballot_response.json()["vote_store_id"]


@pytest.fixture
def ballot_receipt(cast_ballot_response):
    """ballot_check + row_index from a (mocked) cast ballot response"""
    data = cast_ballot_response.json()
    return {
        "ballot_check": data["ballot_check"],
        "row_index": data["ballot_row"],
    }
