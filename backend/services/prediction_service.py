import os
import uuid
import logging
from typing import Dict, Any, List
from fastapi import UploadFile, HTTPException, status

from backend.utils.image_processing import load_and_preprocess_image, bytes_to_base64
from backend.deep_learning.inference import dl_engine
from backend.gradcam.explainer import GradCAMExplainer
from backend.database.repositories.prediction_repository import prediction_repository
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.explainer = None
        if dl_engine.model:
            target_layer = dl_engine.model.get_target_layer()
            self.explainer = GradCAMExplainer(dl_engine.model, target_layer)

    async def process_medical_image(
        self,
        file: UploadFile,
        user_id: str,
        organ_system: str = "Chest Radiograph"
    ) -> Dict[str, Any]:
        
        # Validate content type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File provided is not a valid medical image format."
            )

        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image file exceeds maximum allowable size of {settings.MAX_UPLOAD_SIZE_MB}MB."
            )

        # 1. Preprocess image
        pil_img, tensor_img, cv2_img_bgr = load_and_preprocess_image(content)

        # 2. Run Deep Learning inference
        prediction_result = dl_engine.predict(tensor_img)

        # 3. Convert original image to base64 image URL
        image_url = bytes_to_base64(content, file.content_type)

        # 4. Generate Grad-CAM Heatmap Visualization
        gradcam_url = None
        if self.explainer:
            try:
                # Find index of predicted top class
                predicted_class = prediction_result["predicted_class"]
                class_idx = dl_engine.classes.index(predicted_class) if predicted_class in dl_engine.classes else 0
                gradcam_url = self.explainer.generate_heatmap(
                    tensor_img=tensor_img,
                    cv2_img_bgr=cv2_img_bgr,
                    target_class_idx=class_idx,
                    alpha=0.5
                )
            except Exception as e:
                logger.error(f"Grad-CAM generation error: {e}")
                gradcam_url = image_url  # Fallback to original

        prediction_id = str(uuid.uuid4())
        record = {
            "_id": prediction_id,
            "user_id": user_id,
            "image_name": file.filename,
            "image_url": image_url,
            "predicted_class": prediction_result["predicted_class"],
            "confidence": prediction_result["confidence"],
            "all_probabilities": prediction_result["all_probabilities"],
            "gradcam_heatmap_url": gradcam_url,
            "organ_system": organ_system,
            "status": "completed"
        }

        # 5. Persist prediction in repository
        saved_record = await prediction_repository.create(record)
        
        # Rename _id to id for API response
        saved_record["id"] = saved_record["_id"]
        return saved_record

    async def get_user_history(self, user_id: str, limit: int = 50, skip: int = 0) -> List[Dict[str, Any]]:
        scans = await prediction_repository.get_by_user(user_id=user_id, limit=limit, skip=skip)
        for s in scans:
            s["id"] = s.get("_id", s.get("id"))
        return scans

    async def delete_prediction(self, prediction_id: str, user_id: str) -> bool:
        prediction = await prediction_repository.get_by_id(prediction_id)
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction scan record not found.")
        if prediction.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized to delete this prediction record.")
        
        return await prediction_repository.delete(prediction_id)

prediction_service = PredictionService()
