import json
import logging
from typing import Dict, Any, List
from backend.config.settings import settings
from backend.llm.base import BaseLLMProvider
from backend.llm.mock_provider import MockLLMProvider

logger = logging.getLogger(__name__)

class GeminiLLMProvider(BaseLLMProvider):
    """
    LLM Medical Report Generator powered by Google Gemini API.
    """
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.fallback_provider = MockLLMProvider()
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Successfully configured Gemini API provider.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini API: {e}. Will use fallback provider.")
                self.model = None
        else:
            self.model = None

    async def generate_medical_report(
        self,
        predicted_class: str,
        confidence: float,
        all_probabilities: List[Dict[str, Any]],
        patient_id: str = "P-100234",
        organ_system: str = "Chest Radiograph",
        clinical_context: str = ""
    ) -> Dict[str, Any]:
        if not self.model or not self.api_key:
            logger.info("Gemini API key missing or uninitialized. Using mock report generator.")
            return await self.fallback_provider.generate_medical_report(
                predicted_class, confidence, all_probabilities, patient_id, organ_system, clinical_context
            )

        prompt = f"""
You are an expert Board-Certified Radiologist and Clinical AI Consultant.
Generate a structured medical diagnostic summary report based on the following AI visual analysis of a {organ_system}:

Patient ID: {patient_id}
Top Predicted Finding: {predicted_class}
Confidence Score: {confidence}%
Class Probabilities: {json.dumps(all_probabilities)}
Clinical Context: {clinical_context or 'Routine diagnostic evaluation'}

Respond ONLY with a valid JSON object matching this exact key structure:
{{
  "summary": "Clinical overview paragraph...",
  "prediction_findings": "Detailed description of AI findings...",
  "confidence_assessment": "Explanation of statistical confidence...",
  "possible_causes": ["Cause 1", "Cause 2"],
  "risk_factors": ["Risk factor 1", "Risk factor 2"],
  "symptoms_checklist": ["Symptom 1", "Symptom 2"],
  "precautions": ["Precaution 1", "Precaution 2"],
  "lifestyle_advice": ["Advice 1", "Advice 2"],
  "recommended_consultation": "Recommended medical specialist",
  "disclaimer": "AI report advisory statement..."
}}
"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            report_dict = json.loads(response.text)
            return report_dict
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}. Falling back to mock provider.")
            return await self.fallback_provider.generate_medical_report(
                predicted_class, confidence, all_probabilities, patient_id, organ_system, clinical_context
            )
