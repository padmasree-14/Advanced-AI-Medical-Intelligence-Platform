from typing import Dict, Any, List
from backend.llm.base import BaseLLMProvider

class MockLLMProvider(BaseLLMProvider):
    """
    Offline/Fallback Medical Report Generator providing structured, clinically aligned report content.
    """
    async def generate_medical_report(
        self,
        predicted_class: str,
        confidence: float,
        all_probabilities: List[Dict[str, Any]],
        patient_id: str = "P-100234",
        organ_system: str = "Chest Radiograph",
        clinical_context: str = ""
    ) -> Dict[str, Any]:
        
        prob_summary = ", ".join([f"{p['class_name']}: {p['confidence']}%" for p in all_probabilities])

        if predicted_class.lower() == "normal":
            summary = "Chest radiograph analysis reveals clear pulmonary fields with no acute focal consolidation, pleural effusion, or pneumothorax."
            prediction_findings = f"Automated AI visual analysis indicates Normal chest anatomy with a confidence of {confidence}%."
            confidence_assessment = f"High confidence ({confidence}%). Visual feature heatmaps align with bilateral clear pulmonary parenchyma."
            possible_causes = ["Unremarkable radiographic examination", "Absence of acute infectious process"]
            risk_factors = ["Minimal risk under current evaluation. Maintain routine preventative wellness visits."]
            symptoms_checklist = ["No dyspnea reported", "No acute fever", "Normal oxygen saturation"]
            precautions = ["Maintain healthy lifestyle", "Schedule routine annual health checkup"]
            lifestyle_advice = ["Maintain balanced diet and hydration", "Regular physical activity", "Avoid active and passive tobacco smoke exposure"]
            recommended_consultation = "Primary Care Physician routine review"
        elif predicted_class.lower() == "pneumonia":
            summary = "Radiographic pattern shows localized opacity and airspace consolidation suggestive of inflammatory parenchymal infiltration characteristic of pneumonia."
            prediction_findings = f"Deep learning model detected patterns consistent with Pneumonia with a confidence of {confidence}%."
            confidence_assessment = f"Diagnostic confidence is {confidence}%. Differential probability distribution: {prob_summary}."
            possible_causes = ["Bacterial lower respiratory tract infection (e.g. Streptococcus pneumoniae)", "Viral pneumonia", "Atypical mycoplasma infection"]
            risk_factors = ["Recent upper respiratory tract infection", "Immunocompromised status", "Tobacco smoke exposure", "Advanced age or chronic pulmonary disease"]
            symptoms_checklist = ["Productive or persistent cough", "Fever and chills", "Pleuritic chest pain", "Shortness of breath / dyspnea"]
            precautions = ["Seek prompt clinical evaluation", "Rest and elevate head during sleep", "Monitor body temperature and pulse oximetry"]
            lifestyle_advice = ["Increase fluid intake to thin bronchial secretions", "Avoid respiratory irritants", "Complete prescribed antimicrobial course if indicated"]
            recommended_consultation = "Pulmonologist or Urgent Care Physician for clinical evaluation and sputum/blood work"
        elif predicted_class.lower() == "tuberculosis":
            summary = "Radiographic scan exhibits apical pulmonary parenchymal opacity, cavitation, or hilar lymphadenopathy suggestive of Mycobacterium tuberculosis involvement."
            prediction_findings = f"Deep learning model identified features consistent with Tuberculosis with a confidence of {confidence}%."
            confidence_assessment = f"Confidence level is {confidence}%. Further microbiological testing (Sputum AFB smear / GeneXpert) is recommended."
            possible_causes = ["Mycobacterium tuberculosis infection", "Reactivation of latent TB infection"]
            risk_factors = ["Close contact with active TB cases", "Immunosuppression (e.g. HIV, chronic steroid use)", "Malnutrition or crowded living conditions"]
            symptoms_checklist = ["Chronic cough lasting > 3 weeks", "Night sweats", "Unexplained weight loss", "Low-grade evening fever", "Hemoptysis"]
            precautions = ["Strict respiratory isolation / wear N95 mask around others", "Adhere to strict anti-TB drug therapy (DOTS)", "Monitor hepatic function"]
            lifestyle_advice = ["High-protein nutritional support", "Adequate ventilation in living spaces", "Complete multi-month treatment regimen without interruption"]
            recommended_consultation = "Infectious Disease Specialist & Public Health Tuberculosis Clinic"
        else: # COVID-19 or general
            summary = "Radiographs demonstrate bilateral peripheral, lower-zone predominant ground-glass opacities consistent with viral pneumonitis."
            prediction_findings = f"Deep learning diagnostic engine detected viral pulmonary involvement consistent with COVID-19 at {confidence}% confidence."
            confidence_assessment = f"Model output indicates {confidence}% confidence. Correlate with RT-PCR or rapid antigen testing."
            possible_causes = ["SARS-CoV-2 viral infection", "Secondary pulmonary inflammatory response"]
            risk_factors = ["Exposure to confirmed COVID-19 cases", "Lack of vaccination/boosters", "Pre-existing cardiovascular or pulmonary comorbidities"]
            symptoms_checklist = ["Fever or chills", "Dry cough", "Anosmia / ageusia (loss of taste/smell)", "Fatigue and myalgia"]
            precautions = ["Self-isolate in accordance with local health guidelines", "Monitor blood oxygen (SpO2) frequently", "Stay well-hydrated"]
            lifestyle_advice = ["Prone positioning if experiencing mild hypoxia", "Adequate rest", "Antipyretic therapy as guided by physician"]
            recommended_consultation = "Primary Care Provider or COVID-19 Telehealth Specialist"

        return {
            "summary": summary,
            "prediction_findings": prediction_findings,
            "confidence_assessment": confidence_assessment,
            "possible_causes": possible_causes,
            "risk_factors": risk_factors,
            "symptoms_checklist": symptoms_checklist,
            "precautions": precautions,
            "lifestyle_advice": lifestyle_advice,
            "recommended_consultation": recommended_consultation,
            "disclaimer": "IMPORTANT NOTICE: This AI-generated medical report is produced by an automated deep learning decision-support tool for educational and preliminary screening purposes only. It does not replace professional clinical evaluation, radiologist interpretation, or diagnostic laboratory testing."
        }
