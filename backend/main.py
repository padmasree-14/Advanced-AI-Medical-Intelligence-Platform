import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from backend.config.settings import settings
from backend.database.mongo import db_manager
from backend.middlewares.logging import RequestLoggingMiddleware
from backend.routers import auth_router, prediction_router, report_router, profile_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    logger.info("Initializing Advanced AI Medical Intelligence Platform Backend...")
    await db_manager.connect()
    yield
    # Shutdown tasks
    logger.info("Shutting down backend services...")
    await db_manager.close()

app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise API platform for Medical Image Classification, Grad-CAM Explainable AI, and LLM Report Generation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Custom CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Audit Middleware
app.add_middleware(RequestLoggingMiddleware)

# Include API Routers with Prefix
app.include_router(auth_router.router, prefix=settings.API_V1_STR)
app.include_router(prediction_router.router, prefix=settings.API_V1_STR)
app.include_router(report_router.router, prefix=settings.API_V1_STR)
app.include_router(profile_router.router, prefix=settings.API_V1_STR)

# Serve built React frontend static files
FRONTEND_DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.isdir(FRONTEND_DIST_DIR):
    # Mount static assets (JS, CSS, images) under /assets
    assets_dir = os.path.join(FRONTEND_DIST_DIR, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        """Serve the React SPA - serves index.html for all non-API routes."""
        # Check if a specific static file exists (e.g., favicon, manifest)
        file_path = os.path.join(FRONTEND_DIST_DIR, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        # Otherwise serve index.html for React Router client-side routing
        index_path = os.path.join(FRONTEND_DIST_DIR, "index.html")
        if os.path.isfile(index_path):
            return FileResponse(index_path)
        return JSONResponse({"detail": "Not found"}, status_code=404)
else:
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "title": settings.APP_NAME,
            "status": "Online",
            "docs_url": "/docs",
            "api_v1": settings.API_V1_STR
        }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled system error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": "An internal server error occurred.", "error": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
