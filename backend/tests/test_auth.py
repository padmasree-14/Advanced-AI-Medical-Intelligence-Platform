import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app

@pytest.mark.asyncio
async def test_user_registration_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register user
        register_payload = {
            "email": "test.radiologist@hospital.org",
            "username": "testradio",
            "password": "SecretPassword123!",
            "full_name": "Dr. Test Radiologist",
            "role": "radiologist"
        }
        res = await ac.post("/api/v1/auth/register", json=register_payload)
        assert res.status_code == 201
        data = res.json()
        assert data["success"] is True
        assert data["data"]["email"] == "test.radiologist@hospital.org"

        # Login user
        login_payload = {
            "username_or_email": "testradio",
            "password": "SecretPassword123!"
        }
        res_login = await ac.post("/api/v1/auth/login", json=login_payload)
        assert res_login.status_code == 200
        token_data = res_login.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
