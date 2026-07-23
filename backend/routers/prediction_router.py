from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, Form, status, Query
from backend.middlewares.auth import get_current_user
from backend.schemas.dto import PredictionResponse, StandardResponse
from backend.services.prediction_service import prediction_service
from backend.services.audit_service import audit_service

router = APIRouter(tags=["Predictions"])

@router.post("/predict", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def predict_medical_image(
    file: UploadFile = File(...),
    organ_system: Optional[str] = Form("Chest Radiograph"),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["_id"]
    result = await prediction_service.process_medical_image(
        file=file,
        user_id=user_id,
        organ_system=organ_system
    )
    await audit_service.log_action("IMAGE_PREDICT", "predictions", user_id=user_id, details={"prediction_id": result["id"]})
    return StandardResponse(
        success=True,
        message="Medical image analyzed successfully.",
        data=result
    )

@router.get("/history", response_model=StandardResponse)
async def get_prediction_history(
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["_id"]
    history = await prediction_service.get_user_history(user_id=user_id, limit=limit, skip=skip)
    return StandardResponse(
        success=True,
        message="Prediction history retrieved successfully.",
        data=history
    )

@router.delete("/history/{id}", response_model=StandardResponse)
async def delete_history_item(
    id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["_id"]
    success = await prediction_service.delete_prediction(prediction_id=id, user_id=user_id)
    await audit_service.log_action("DELETE_PREDICTION", "predictions", user_id=user_id, details={"prediction_id": id})
    return StandardResponse(
        success=success,
        message="Prediction scan record deleted successfully."
    )
