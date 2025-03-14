"""
Controller for handling API requests related to audio extraction.
"""
import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends, status
from fastapi.responses import JSONResponse, FileResponse

from app.features.audio_extraction.services.audio_extraction_service import AudioExtractionService
from app.features.audio_extraction.models.audio_extraction_model import AudioExtractionResult, AudioExtractionRequest
from app.infrastructure.storage.storage_service import StorageService
from app.shared.exceptions.audio_extraction_exceptions import (
    InvalidFileTypeError, FileSizeLimitExceededError, ConversionError, StorageError
)


# Router for audio extraction endpoints
router = APIRouter(
    prefix="/audio-extraction",
    tags=["audio-extraction"],
    responses={404: {"description": "Not found"}}
)


def get_storage_service():
    """Dependency for getting a storage service instance."""
    return StorageService(base_directory="storage")


def get_extraction_service(storage_service: StorageService = Depends(get_storage_service)):
    """Dependency for getting an audio extraction service instance."""
    return AudioExtractionService(storage_service=storage_service)


@router.post("/upload", response_model=AudioExtractionResult, status_code=status.HTTP_202_ACCEPTED)
async def upload_and_extract(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    extraction_service: AudioExtractionService = Depends(get_extraction_service),
    storage_service: StorageService = Depends(get_storage_service)
):
    """
    Upload a video file and extract audio from it.
    
    The extraction is performed asynchronously in a background task.
    
    Args:
        background_tasks: Background tasks object for async processing
        file: The video file to upload
        extraction_service: The extraction service
        storage_service: The storage service
        
    Returns:
        Information about the extraction job
    """
    try:
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower().lstrip(".")
        # Save the uploaded file
        file_id = f"{os.path.splitext(file.filename)[0]}_{os.urandom(4).hex()}.{file_ext}"
        file_path = storage_service.get_file_path(file_id)
        
        # Read file content
        file_content = await file.read()
        
        # Save the file
        storage_service.save_file(file_content, file_path)
        
        # Start background task for extraction
        result = extraction_service.extract_audio_from_video(file_path)
        
        return result
        
    except InvalidFileTypeError as e:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=e.message
        )
    except FileSizeLimitExceededError as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=e.message
        )
    except (ConversionError, StorageError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/status/{job_id}", response_model=AudioExtractionResult)
async def get_extraction_status(
    job_id: str,
    extraction_service: AudioExtractionService = Depends(get_extraction_service)
):
    """
    Get the status of an audio extraction job.
    
    Args:
        job_id: The ID of the extraction job
        extraction_service: The extraction service
        
    Returns:
        Information about the extraction job
    """
    try:
        result = extraction_service.get_extraction_status(job_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} not found"
            )
        
        return result
    except StorageError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/download/{job_id}")
async def download_audio(
    job_id: str,
    extraction_service: AudioExtractionService = Depends(get_extraction_service)
):
    """
    Download the extracted audio file.
    
    Args:
        job_id: The ID of the extraction job
        extraction_service: The extraction service
        
    Returns:
        The audio file
    """
    try:
        result = extraction_service.get_extraction_status(job_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} not found"
            )
        
        if result.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job is not completed yet. Current status: {result.status}"
            )
        
        if not result.output_path or not os.path.exists(result.output_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Output file not found"
            )
        
        return FileResponse(
            path=result.output_path,
            media_type="audio/mpeg",
            filename=f"{os.path.splitext(result.original_filename)[0]}.{result.output_format}"
        )
    except StorageError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )