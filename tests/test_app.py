import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

@pytest.mark.asyncio
async def test_signup_and_unregister():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Sign up a new participant
        response = await ac.post("/activities/Basketball Team/signup?email=tester@mergington.edu")
        assert response.status_code == 200
        # Check participant is in the list
        response = await ac.get("/activities")
        participants = response.json()["Basketball Team"]["participants"]
        assert "tester@mergington.edu" in participants
        # Unregister the participant
        response = await ac.post("/activities/Basketball Team/unregister", json={"email": "tester@mergington.edu"})
        assert response.status_code == 200
        # Check participant is removed
        response = await ac.get("/activities")
        participants = response.json()["Basketball Team"]["participants"]
        assert "tester@mergington.edu" not in participants
