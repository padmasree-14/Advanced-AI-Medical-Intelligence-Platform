from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr

class UserInDB(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    username: str
    full_name: str
    hashed_password: str
    role: str = "radiologist"  # radiologist, physician, admin
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class PredictionClassDetail(BaseModel):
    class_name: str
    confidence: float

class PredictionInDB(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    image_name: str
    image_url: str
    predicted_class: str
    confidence: float
    all_probabilities: List[PredictionClassDetail]
    gradcam_heatmap_url: Optional[str] = None
    organ_system: str = "Chest Radiograph"
    status: str = "completed"  # pending, completed, failed
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class MedicalReportInDB(BaseModel):
    id: str = Field(alias="_id")
    prediction_id: str
    user_id: str
    patient_id: Optional[str] = "P-100234"
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
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class AuditLogInDB(BaseModel):
    id: str = Field(alias="_id")
    user_id: Optional[str] = None
    action: str
    resource: str
    ip_address: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
