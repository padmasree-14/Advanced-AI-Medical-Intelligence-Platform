from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_medical_report(
        self,
        predicted_class: str,
        confidence: float,
        all_probabilities: List[Dict[str, Any]],
        patient_id: str = "P-100234",
        organ_system: str = "Chest Radiograph",
        clinical_context: str = ""
    ) -> Dict[str, Any]:
        """
        Generates a comprehensive clinical medical report based on Deep Learning findings.
        Returns dictionary matching MedicalReportInDB / DTO schema.
        """
        pass
