from fastapi import APIRouter, Depends, status
from backend.middlewares.auth import get_current_user
from backend.schemas.dto import ReportGenerateRequest, MedicalReportResponse, StandardResponse
from backend.services.report_service import report_service
from backend.services.audit_service import audit_service

router = APIRouter(tags=["Medical Reports"])

@router.post("/generate-report", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def generate_medical_report(
    req: ReportGenerateRequest,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["_id"]
    report = await report_service.generate_report_for_prediction(req=req, user_id=user_id)
    await audit_service.log_action("GENERATE_REPORT", "reports", user_id=user_id, details={"report_id": report["id"]})
    return StandardResponse(
        success=True,
        message="AI Medical report generated successfully.",
        data=report
    )

@router.get("/report/{prediction_id}", response_model=StandardResponse)
async def get_report(
    prediction_id: str,
    current_user: dict = Depends(get_current_user)
):
    report = await report_service.get_report_by_prediction_id(prediction_id=prediction_id)
    return StandardResponse(
        success=True,
        message="Medical report retrieved.",
        data=report
    )
