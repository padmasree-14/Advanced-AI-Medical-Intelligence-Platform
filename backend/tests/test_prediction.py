import io
import pytest
from PIL import Image
from httpx import AsyncClient, ASGITransport
from backend.main import app

def create_sample_image_bytes():
    img = Image.new('RGB', (224, 224), color = (100, 100, 100))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()

@pytest.mark.asyncio
async def test_prediction_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register and login to get JWT
        reg_payload = {
            "email": "pred.user@hospital.org",
            "username": "preduser",
            "password": "Password123!",
            "full_name": "Dr. Pred User"
        }
        await ac.post("/api/v1/auth/register", json=reg_payload)
        login_res = await ac.post("/api/v1/auth/login", json={"username_or_email": "preduser", "password": "Password123!"})
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Upload image for prediction
        img_bytes = create_sample_image_bytes()
        files = {"file": ("chest_xray.jpg", img_bytes, "image/jpeg")}
        data = {"organ_system": "Chest Radiograph"}

        res = await ac.post("/api/v1/predict", headers=headers, files=files, data=data)
        assert res.status_code == 201
        res_json = res.json()
        assert res_json["success"] is True
        assert "predicted_class" in res_json["data"]
        assert "confidence" in res_json["data"]
        assert "gradcam_heatmap_url" in res_json["data"]

        # Fetch history
        res_hist = await ac.get("/api/v1/history", headers=headers)
        assert res_hist.status_code == 200
        assert len(res_hist.json()["data"]) >= 1
