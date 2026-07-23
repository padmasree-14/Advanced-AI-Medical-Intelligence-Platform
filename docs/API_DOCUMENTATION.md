# API Documentation - Advanced AI Medical Intelligence Platform

## Overview
The Advanced AI Medical Intelligence Platform backend provides a high-performance RESTful API powered by FastAPI.
All requests require JSON payloads unless otherwise specified (e.g. multipart/form-data for image uploads).
Protected endpoints require a valid JWT Bearer token supplied in the `Authorization` header (`Authorization: Bearer <TOKEN>`).

---

## Authentication Endpoints

### 1. User Registration
- **Endpoint**: `POST /api/v1/auth/register`
- **Auth**: None
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "email": "radiologist@hospital.org",
    "username": "dr_smith",
    "password": "SecurePassword123!",
    "full_name": "Dr. John Smith, MD",
    "role": "radiologist"
  }
  ```
- **Success Response (201 Created)**:
  ```json
  {
    "success": true,
    "message": "User registered successfully.",
    "data": {
      "id": "u-991203",
      "email": "radiologist@hospital.org",
      "username": "dr_smith",
      "full_name": "Dr. John Smith, MD",
      "role": "radiologist"
    }
  }
  ```

### 2. User Login
- **Endpoint**: `POST /api/v1/auth/login`
- **Auth**: None
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "username_or_email": "dr_smith",
    "password": "SecurePassword123!"
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
      "id": "u-991203",
      "email": "radiologist@hospital.org",
      "username": "dr_smith",
      "full_name": "Dr. John Smith, MD",
      "role": "radiologist"
    }
  }
  ```

---

## Diagnostic Prediction Endpoints

### 3. Medical Image Classification & Grad-CAM Analysis
- **Endpoint**: `POST /api/v1/predict`
- **Auth**: Bearer Token
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: Medical radiograph image binary (JPEG, PNG, DICOM)
  - `organ_system`: "Chest Radiograph" (Optional)
- **Success Response (201 Created)**:
  ```json
  {
    "success": true,
    "message": "Medical image analyzed successfully.",
    "data": {
      "id": "pred-49102",
      "user_id": "u-991203",
      "image_name": "patient_chest_xray.jpg",
      "image_url": "data:image/jpeg;base64,...",
      "predicted_class": "Pneumonia",
      "confidence": 97.4,
      "all_probabilities": [
        { "class_name": "Pneumonia", "confidence": 97.4 },
        { "class_name": "Normal", "confidence": 1.8 },
        { "class_name": "COVID-19", "confidence": 0.5 },
        { "class_name": "Tuberculosis", "confidence": 0.3 }
      ],
      "gradcam_heatmap_url": "data:image/jpeg;base64,...",
      "organ_system": "Chest Radiograph",
      "status": "completed",
      "created_at": "2026-07-23T11:00:00Z"
    }
  }
  ```

### 4. Fetch Prediction History
- **Endpoint**: `GET /api/v1/history`
- **Auth**: Bearer Token
- **Query Parameters**: `limit` (default: 50), `skip` (default: 0)
- **Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Prediction history retrieved successfully.",
    "data": [ ... ]
  }
  ```

### 5. Delete Prediction Scan Record
- **Endpoint**: `DELETE /api/v1/history/{id}`
- **Auth**: Bearer Token
- **Success Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Prediction scan record deleted successfully."
  }
  ```

---

## AI Medical Report Endpoints

### 6. Generate Clinical Medical Report
- **Endpoint**: `POST /api/v1/generate-report`
- **Auth**: Bearer Token
- **Request Body**:
  ```json
  {
    "prediction_id": "pred-49102",
    "patient_id": "P-100234",
    "clinical_context": "Chest radiograph for acute dyspnea"
  }
  ```
- **Success Response (201 Created)**:
  ```json
  {
    "success": true,
    "message": "AI Medical report generated successfully.",
    "data": {
      "id": "rep-88123",
      "prediction_id": "pred-49102",
      "patient_id": "P-100234",
      "summary": "Radiographic scan indicates acute airspace consolidation...",
      "prediction_findings": "Deep learning model detected Pneumonia at 97.4% confidence.",
      "confidence_assessment": "High confidence (97.4%).",
      "possible_causes": [ "Bacterial lower respiratory tract infection" ],
      "risk_factors": [ "Advanced age", "Tobacco smoke exposure" ],
      "symptoms_checklist": [ "Fever", "Productive cough" ],
      "precautions": [ "Seek prompt clinical evaluation" ],
      "lifestyle_advice": [ "Adequate hydration and rest" ],
      "recommended_consultation": "Pulmonologist evaluation",
      "disclaimer": "AI medical report advisory statement..."
    }
  }
  ```

---

## User Profile & Health Endpoints

### 7. Fetch Profile
- **Endpoint**: `GET /api/v1/profile`
- **Auth**: Bearer Token

### 8. Fetch Dashboard Analytics
- **Endpoint**: `GET /api/v1/dashboard-stats`
- **Auth**: Bearer Token

### 9. System Health Check
- **Endpoint**: `GET /api/v1/health`
- **Auth**: None
