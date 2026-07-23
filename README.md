# Advanced AI Medical Intelligence Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C.svg?style=flat-square&logo=pytorch)](https://pytorch.org/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg?style=flat-square&logo=react)](https://reactjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3-38B2AC.svg?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat-square&logo=docker)](https://www.docker.com/)

An enterprise-grade, end-to-end AI Medical Intelligence Platform designed for medical image classification, Explainable AI visual heatmap generation (Grad-CAM), and automated clinical report generation powered by Google Gemini LLM.

---

## 🌟 Key Features

- **Medical Image Classification**: EfficientNet-B0 transfer learning model tuned for multi-class chest radiograph diagnoses (*Normal*, *Pneumonia*, *Tuberculosis*, *COVID-19*).
- **Explainable AI (Grad-CAM)**: Visual activation heatmaps highlighting target neural decision regions with interactive intensity sliders.
- **LLM Medical Report Synthesis**: Automated clinical summary report generation using Gemini API (with offline mock provider fallback).
- **Modern React Frontend**: Modern dark-mode interface built with React 18, Tailwind CSS, Lucide Icons, and Recharts analytics.
- **FastAPI Modular Architecture**: Repository Pattern, Pydantic DTO schemas, JWT authentication, and request audit logging.
- **MongoDB Atlas Storage**: Async PyMongo database storage for users, predictions, reports, and audit logs.
- **Docker Containerization**: Multi-stage `Dockerfile` and `docker-compose.yml` configuration for seamless deployment.

---

## 🛠 Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, Axios, React Router v6, Recharts, Lucide Icons |
| **Backend** | FastAPI, Python 3.10, Pydantic v2, Passlib (Bcrypt), PyJWT |
| **Deep Learning** | PyTorch, torchvision (EfficientNet-B0), OpenCV, Pillow, scikit-learn |
| **Explainable AI** | Grad-CAM (Target Layer Forward/Backward PyTorch Hooks) |
| **LLM Service** | Google Gemini API (`gemini-1.5-flash`) / Mock Provider Fallback |
| **Database** | MongoDB Atlas (Async Motor / PyMongo Driver) |
| **Deployment** | Docker, docker-compose, Vercel, Render |

---

## 📁 Repository Structure

```
.
├── backend/
│   ├── config/             # Settings & Environment variables
│   ├── database/           # MongoDB client & Repository Pattern classes
│   ├── deep_learning/      # PyTorch EfficientNet-B0 model & inference engine
│   ├── gradcam/            # Grad-CAM heatmap explainer engine
│   ├── llm/                # Gemini & Mock LLM provider implementations
│   ├── middlewares/        # JWT Auth & Audit logging middlewares
│   ├── models/             # Domain data models & MongoDB schemas
│   ├── routers/            # FastAPI REST API endpoints
│   ├── schemas/            # Pydantic DTOs for requests and responses
│   ├── services/           # Core business logic layer
│   ├── tests/              # Pytest automated test suites
│   └── utils/              # Security (Bcrypt/JWT) & image processing helpers
├── training/               # Model training loop, dataset generator & metrics script
├── frontend/               # React 18 + Vite + Tailwind CSS application
├── deployment/             # Dockerfiles, docker-compose.yml, Vercel & Render configs
├── docs/                   # API Documentation & Technical Project Report
├── requirements.txt        # Python backend dependencies
├── .env.example            # Blueprint environment variables file
└── README.md               # Enterprise documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (Local or MongoDB Atlas connection URL)

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/organization/ai-medical-intelligence.platform.git
cd ai-medical-intelligence.platform

# Copy environment variables
cp .env.example .env

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
Backend API will be accessible at: `http://localhost:8000` (OpenAPI Docs: `http://localhost:8000/docs`).

### 2. Frontend Setup

```bash
cd frontend

# Install frontend dependencies
npm install

# Launch Vite development server
npm run dev
```
Frontend Web Dashboard will be accessible at: `http://localhost:5173`.

---

## 🔬 Training & Model Evaluation

```bash
# Generate synthetic dataset and execute training loop
python training/train.py

# Evaluate model metrics (Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix)
python training/evaluate.py
```

---

## 🐳 Docker Deployment

```bash
# Launch entire stack via Docker Compose
docker-compose -f deployment/docker-compose.yml up --build -d
```

---

## 🧪 Running Tests

```bash
# Run pytest suite
pytest backend/tests/
```

---

## 📜 License & Medical Disclaimer
This software is provided for educational, research, and decision-support purposes. All AI predictions and reports should be corroborated by board-certified clinical professionals.
