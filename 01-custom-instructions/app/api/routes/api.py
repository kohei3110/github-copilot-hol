"""
API routes configuration.
"""
from fastapi import APIRouter

from app.features.audio_extraction.controllers.audio_extraction_controller import router as audio_extraction_router


# Main API router
api_router = APIRouter()

# Include feature routers
api_router.include_router(audio_extraction_router)