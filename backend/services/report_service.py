import uuid
import logging
from typing import Dict, Any
from fastapi import HTTPException, status

from backend.database.repositories.prediction_repository import prediction_repository
from backend.database.repositories.report_repository import report_repository
from backend.llm.factory import get_llm_provider
from backend.schemas.dto import ReportGenerateRequest

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self):
        self.llm_provider = get_llm_provider()

    async def generate_report_for_prediction(self, req: ReportGenerateRequest, user_id: str) -> Dict[str, Any]:
        # 1. Fetch prediction record
        prediction = await prediction_repository.get_by_id(req.prediction_id)
        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target prediction scan not found."
            )

        # Check existing report
        existing = await report_repository.get_by_prediction_id(req.prediction_id)
        if existing:
            existing["id"] = existing.get("_id", existing.get("id"))
            return existing

        # 2. Call LLM provider
        report_data = await self.llm_provider.generate_medical_report(
            predicted_class=prediction["predicted_class"],
            confidence=prediction["confidence"],
            all_probabilities=prediction["all_probabilities"],
            patient_id=req.patient_id or "P-100234",
            organ_system=prediction.get("organ_system", "Chest Radiograph"),
            clinical_context=req.clinical_context or ""
        )

        # 3. Form report record
        report_id = str(uuid.uuid4())
        record = {
            "_id": report_id,
            "prediction_id": req.prediction_id,
            "user_id": user_id,
            "patient_id": req.patient_id or "P-100234",
            "summary": report_data.get("summary", ""),
            "prediction_findings": report_data.get("prediction_findings", ""),
            "confidence_assessment": report_data.get("confidence_assessment", ""),
            "possible_causes": report_data.get("possible_causes", []),
            "risk_factors": report_data.get("risk_factors", []),
            "symptoms_checklist": report_data.get("symptoms_checklist", []),
            "precautions": report_data.get("precautions", []),
            "lifestyle_advice": report_data.get("lifestyle_advice", []),
            "recommended_consultation": report_data.get("recommended_consultation", ""),
            "disclaimer": report_data.get("disclaimer", "")
        }

        # 4. Save report in database
        saved_report = await report_repository.create(record)
        saved_report["id"] = saved_report["_id"]
        return saved_report

    async def get_report_by_prediction_id(self, prediction_id: str) -> Dict[str, Any]:
        report = await report_repository.get_by_prediction_id(prediction_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical report not found for this prediction."
            )
        report["id"] = report.get("_id", report.get("id"))
        return report

report_service = ReportService()
