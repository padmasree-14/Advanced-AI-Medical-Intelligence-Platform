from datetime import datetime
from fastapi import APIRouter, Depends
from backend.middlewares.auth import get_current_user
from backend.schemas.dto import StandardResponse
from backend.database.repositories.prediction_repository import prediction_repository
from backend.database.mongo import db_manager
from backend.config.settings import settings

router = APIRouter(tags=["User Profile & System"])

@router.get("/profile", response_model=StandardResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    total_scans = await prediction_repository.count_by_user(user_id)
    profile_data = {
        "id": current_user["_id"],
        "email": current_user["email"],
        "username": current_user["username"],
        "full_name": current_user["full_name"],
        "role": current_user.get("role", "radiologist"),
        "is_active": current_user.get("is_active", True),
        "created_at": current_user.get("created_at", datetime.utcnow()),
        "total_predictions": total_scans
    }
    return StandardResponse(
        success=True,
        message="Profile details fetched successfully.",
        data=profile_data
    )

@router.get("/dashboard-stats", response_model=StandardResponse)
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    scans = await prediction_repository.get_by_user(user_id=user_id, limit=200)
    
    total_scans = len(scans)
    class_counts = {"Normal": 0, "Pneumonia": 0, "Tuberculosis": 0, "COVID-19": 0}
    total_conf = 0.0

    for scan in scans:
        cls = scan.get("predicted_class", "Normal")
        class_counts[cls] = class_counts.get(cls, 0) + 1
        total_conf += scan.get("confidence", 0.0)

    avg_conf = round(total_conf / total_scans, 2) if total_scans > 0 else 0.0

    # Recent 5 scans formatted
    recent = []
    for s in scans[:5]:
        item = s.copy()
        item["id"] = item.get("_id", item.get("id"))
        recent.append(item)

    stats = {
        "total_scans": total_scans,
        "scans_this_month": total_scans,
        "class_distribution": class_counts,
        "avg_confidence": avg_conf,
        "recent_scans": recent
    }
    
    return StandardResponse(
        success=True,
        message="Dashboard analytics summary.",
        data=stats
    )

@router.get("/health", response_model=StandardResponse)
async def health_check():
    return StandardResponse(
        success=True,
        message="System operational.",
        data={
            "app": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "database_connected": db_manager.is_connected,
            "llm_provider": settings.LLM_PROVIDER,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
