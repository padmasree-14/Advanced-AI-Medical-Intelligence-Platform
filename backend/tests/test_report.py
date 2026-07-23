import io
import pytest
from PIL import Image
from httpx import AsyncClient, ASGITransport
from backend.main import app

@pytest.mark.asyncio
async def test_report_generation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register and authenticate
        await ac.post("/api/v1/auth/register", json={
            "email": "report.user@hospital.org",
            "username": "reportuser",
            "password": "Password123!",
            "full_name": "Dr. Report User"
        })
        login_res = await ac.post("/api/v1/auth/login", json={"username_or_email": "reportuser", "password": "Password123!"})
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Predict image first
        img = Image.new('RGB', (224, 224), color=(120, 120, 120))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        files = {"file": ("report_scan.jpg", buf.getvalue(), "image/jpeg")}
        
        pred_res = await ac.post("/api/v1/predict", headers=headers, files=files)
        pred_id = pred_res.json()["data"]["id"]

        # Generate report
        report_res = await ac.post("/api/v1/generate-report", headers=headers, json={
            "prediction_id": pred_id,
            "patient_id": "P-99881",
            "clinical_context": "Routine check"
        })
        assert report_res.status_code == 201
        report_json = report_res.json()["data"]
        assert "summary" in report_json
        assert "possible_causes" in report_json
        assert "disclaimer" in report_json
