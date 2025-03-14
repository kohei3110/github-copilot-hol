"""
Service for extracting audio from video files.
"""
import os
import uuid
import subprocess
from typing import Optional
from datetime import datetime
import mimetypes

from app.infrastructure.storage.storage_service import StorageService
from app.features.audio_extraction.models.audio_extraction_model import (
    AudioExtractionResult, ProcessingStatus
)
from app.shared.exceptions.audio_extraction_exceptions import (
    InvalidFileTypeError, FileSizeLimitExceededError, ConversionError, StorageError
)
from app.shared.constants.audio_extraction_constants import (
    MAX_FILE_SIZE, SUPPORTED_VIDEO_FORMATS, AUDIO_OUTPUT_FORMAT,
    PROCESSED_DIRECTORY, AUDIO_CONVERSION_SETTINGS
)


class AudioExtractionService:
    """Service for extracting audio from video files."""
    
    def __init__(self, storage_service: StorageService):
        """
        Initialize the audio extraction service.
        
        Args:
            storage_service: The storage service for file operations
        """
        self.storage_service = storage_service
    
    def extract_audio_from_video(self, file_path: str) -> AudioExtractionResult:
        """
        Extract audio from a video file.
        
        Args:
            file_path: The path to the video file
            
        Returns:
            An AudioExtractionResult with information about the extraction
            
        Raises:
            InvalidFileTypeError: If the file is not a supported video format
            FileSizeLimitExceededError: If the file size exceeds the limit
            ConversionError: If there is an error during the extraction
            StorageError: If there is an error with storage operations
        """
        # Check file metadata
        metadata = self.storage_service.get_file_metadata(file_path)
        
        # Validate file type
        file_ext = os.path.splitext(metadata["filename"])[1].lower().lstrip(".")
        if file_ext not in SUPPORTED_VIDEO_FORMATS:
            raise InvalidFileTypeError(file_ext)
        
        # Validate file size
        if metadata["size"] > MAX_FILE_SIZE:
            raise FileSizeLimitExceededError(metadata["size"], MAX_FILE_SIZE)
        
        # Create a job ID for this extraction
        job_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        # Create initial extraction result
        result = AudioExtractionResult(
            job_id=job_id,
            original_filename=metadata["filename"],
            status=ProcessingStatus.PROCESSING,
            output_format=AUDIO_OUTPUT_FORMAT,
            input_size=metadata["size"],
            created_at=now,
            updated_at=now
        )
        
        try:
            # Convert the video to audio
            output_path = self._convert_video_to_audio(file_path, job_id)
            
            # Update the extraction result
            result.status = ProcessingStatus.COMPLETED
            result.output_path = output_path
            result.output_size = self.storage_service.get_file_size(output_path)
            result.updated_at = datetime.now().isoformat()
            
            # Save job data
            self.storage_service.save_extraction_job(result.dict())
            
            return result
        except Exception as e:
            # Update result with error information
            result.status = ProcessingStatus.FAILED
            result.error_message = str(e)
            result.updated_at = datetime.now().isoformat()
            
            # Save job data even if it failed
            try:
                self.storage_service.save_extraction_job(result.dict())
            except Exception:
                pass
            
            # Re-raise the original exception
            if isinstance(e, (InvalidFileTypeError, FileSizeLimitExceededError, ConversionError, StorageError)):
                raise
            raise ConversionError(f"Failed to extract audio: {e}")
    
    def get_extraction_status(self, job_id: str) -> Optional[AudioExtractionResult]:
        """
        Get the status of an audio extraction job.
        
        Args:
            job_id: The ID of the extraction job
            
        Returns:
            The extraction result or None if not found
            
        Raises:
            StorageError: If there is an error accessing job data
        """
        job_data = self.storage_service.get_extraction_job(job_id)
        if not job_data:
            return None
        
        return AudioExtractionResult(**job_data)
    
    def clean_up_old_files(self) -> int:
        """
        Clean up old temporary files.
        
        Returns:
            The number of files deleted
        
        Raises:
            StorageError: If there is an error during cleanup
        """
        old_files = self.storage_service.list_old_files()
        deleted_count = 0
        
        for file_path in old_files:
            self.storage_service.delete_file(file_path)
            deleted_count += 1
        
        return deleted_count
    
    def _convert_video_to_audio(self, input_path: str, job_id: str) -> str:
        """
        Convert a video file to an audio file.
        
        Args:
            input_path: The path to the input video file
            job_id: The ID of the extraction job
            
        Returns:
            The path to the output audio file
            
        Raises:
            ConversionError: If there is an error during conversion
        """
        # Create output directory
        job_dir = os.path.join(self.storage_service.processed_directory, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        # Define output path
        output_path = os.path.join(job_dir, f"audio.{AUDIO_OUTPUT_FORMAT}")
        
        try:
            # Build the ffmpeg command
            command = [
                "ffmpeg",
                "-i", input_path,  # Input file
                "-vn",  # No video
                "-acodec", AUDIO_CONVERSION_SETTINGS["codec"],  # Audio codec
                "-ab", AUDIO_CONVERSION_SETTINGS["bitrate"],  # Audio bitrate
                "-ar", AUDIO_CONVERSION_SETTINGS["sample_rate"],  # Sample rate
                "-ac", AUDIO_CONVERSION_SETTINGS["channels"],  # Channels (mono)
                "-y",  # Overwrite output file if it exists
                output_path  # Output file
            ]
            
            # Run the command
            process = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Check if the output file exists
            if not os.path.exists(output_path):
                stderr = process.stderr.decode('utf-8')
                raise ConversionError(f"Failed to create output file. FFmpeg error: {stderr}")
            
            return output_path
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode('utf-8') if e.stderr else "Unknown error"
            raise ConversionError(f"FFmpeg conversion failed: {stderr}")
        except Exception as e:
            raise ConversionError(f"Error during video to audio conversion: {e}")