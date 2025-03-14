"""
Data models for the audio extraction feature.
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ProcessingStatus(str, Enum):
    """Enum representing the status of audio extraction processing."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AudioExtractionResult(BaseModel):
    """Model representing the result of audio extraction process."""
    job_id: str = Field(..., description="Unique identifier for the extraction job")
    original_filename: str = Field(..., description="Original filename of the uploaded video")
    status: ProcessingStatus = Field(default=ProcessingStatus.PENDING, description="Current status of processing")
    output_format: str = Field(..., description="Format of the output audio file (e.g., mp3)")
    input_size: int = Field(..., description="Size of the input file in bytes")
    output_size: Optional[int] = Field(None, description="Size of the output file in bytes")
    output_path: Optional[str] = Field(None, description="Path to the output audio file")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    created_at: str = Field(..., description="Timestamp when the job was created")
    updated_at: str = Field(..., description="Timestamp when the job was last updated")


class AudioExtractionRequest(BaseModel):
    """Model representing a request for audio extraction."""
    file_id: str = Field(..., description="ID of the uploaded file to process")
    output_format: str = Field("mp3", description="Desired output format for the audio")
    mono: bool = Field(True, description="Whether to convert to mono audio")