from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field

# User Auth Schemas
class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str
    role: Optional[str] = "radiologist"

class UserLoginRequest(BaseModel):
    username_or_email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]

class UserProfileResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    total_predictions: int = 0

# Prediction Schemas
class PredictionClassProbability(BaseModel):
    class_name: str
    confidence: float

class PredictionResponse(BaseModel):
    id: str
    user_id: str
    image_name: str
    image_url: str
    predicted_class: str
    confidence: float
    all_probabilities: List[PredictionClassProbability]
    gradcam_heatmap_url: Optional[str] = None
    organ_system: str
    status: str
    created_at: datetime

class HistoryQueryFilter(BaseModel):
    predicted_class: Optional[str] = None
    limit: int = 50
    skip: int = 0

# Medical Report Schemas
class ReportGenerateRequest(BaseModel):
    prediction_id: str
    patient_id: Optional[str] = "P-100234"
    clinical_context: Optional[str] = ""

class MedicalReportResponse(BaseModel):
    id: str
    prediction_id: str
    user_id: str
    patient_id: str
    summary: str
    prediction_findings: str
    confidence_assessment: str
    possible_causes: List[str]
    risk_factors: List[str]
    symptoms_checklist: List[str]
    precautions: List[str]
    lifestyle_advice: List[str]
    recommended_consultation: str
    disclaimer: str
    created_at: datetime

# Dashboard Statistics Schema
class DashboardStatsResponse(BaseModel):
    total_scans: int
    scans_this_month: int
    class_distribution: Dict[str, int]
    avg_confidence: float
    recent_scans: List[PredictionResponse]

# Generic Response Schema
class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
