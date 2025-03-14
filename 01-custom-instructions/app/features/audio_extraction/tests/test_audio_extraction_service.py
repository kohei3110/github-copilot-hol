"""
Unit tests for the AudioExtractionService.
"""
import os
import uuid
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from app.features.audio_extraction.services.audio_extraction_service import AudioExtractionService
from app.features.audio_extraction.models.audio_extraction_model import AudioExtractionResult, ProcessingStatus
from app.shared.exceptions.audio_extraction_exceptions import (
    InvalidFileTypeError, FileSizeLimitExceededError, ConversionError, StorageError
)
from app.shared.constants.audio_extraction_constants import (
    MAX_FILE_SIZE, SUPPORTED_VIDEO_FORMATS, AUDIO_OUTPUT_FORMAT
)


@pytest.fixture
def audio_extraction_service():
    """Fixture to create an instance of AudioExtractionService for testing."""
    storage_service = MagicMock()
    service = AudioExtractionService(storage_service=storage_service)
    return service, storage_service


@pytest.fixture
def sample_video_file():
    """Fixture to create a sample video file path."""
    return "test_video.mp4"


@pytest.fixture
def sample_extraction_result():
    """Fixture to create a sample AudioExtractionResult."""
    job_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    return AudioExtractionResult(
        job_id=job_id,
        original_filename="test_video.mp4",
        status=ProcessingStatus.COMPLETED,
        output_format="mp3",
        input_size=1024,
        output_size=512,
        output_path=f"processed/{job_id}/audio.mp3",
        created_at=now,
        updated_at=now
    )


class TestAudioExtractionService:
    """Test cases for the AudioExtractionService."""

    def test_extract_audio_from_video_success(self, audio_extraction_service, sample_video_file):
        """Test successful audio extraction from a video file."""
        service, storage_mock = audio_extraction_service
        
        # Mock file metadata
        storage_mock.get_file_metadata.return_value = {
            "filename": sample_video_file,
            "content_type": "video/mp4",
            "size": 1024
        }
        
        # Mock successful conversion
        with patch.object(service, "_convert_video_to_audio") as mock_convert:
            mock_convert.return_value = "processed/some-uuid/audio.mp3"
            
            # Mock file size after conversion
            storage_mock.get_file_size.return_value = 512
            
            # Call the method under test
            result = service.extract_audio_from_video(sample_video_file)
            
            # Assertions
            assert result is not None
            assert result.status == ProcessingStatus.COMPLETED
            assert result.original_filename == sample_video_file
            assert result.output_format == AUDIO_OUTPUT_FORMAT
            assert result.input_size == 1024
            assert result.output_size == 512
            assert result.output_path is not None
            assert mock_convert.called
            
    def test_extract_audio_invalid_file_type(self, audio_extraction_service):
        """Test that an exception is raised for unsupported file types."""
        service, storage_mock = audio_extraction_service
        
        # Mock file metadata for an unsupported type
        storage_mock.get_file_metadata.return_value = {
            "filename": "test.txt",
            "content_type": "text/plain",
            "size": 1024
        }
        
        # Call the method and expect an exception
        with pytest.raises(InvalidFileTypeError):
            service.extract_audio_from_video("test.txt")
            
    def test_extract_audio_size_limit_exceeded(self, audio_extraction_service):
        """Test that an exception is raised when file size exceeds the limit."""
        service, storage_mock = audio_extraction_service
        
        # Mock file metadata with a size exceeding the limit
        storage_mock.get_file_metadata.return_value = {
            "filename": "large_video.mp4",
            "content_type": "video/mp4",
            "size": MAX_FILE_SIZE + 1
        }
        
        # Call the method and expect an exception
        with pytest.raises(FileSizeLimitExceededError):
            service.extract_audio_from_video("large_video.mp4")
            
    def test_extract_audio_conversion_error(self, audio_extraction_service, sample_video_file):
        """Test handling of conversion errors."""
        service, storage_mock = audio_extraction_service
        
        # Mock file metadata
        storage_mock.get_file_metadata.return_value = {
            "filename": sample_video_file,
            "content_type": "video/mp4",
            "size": 1024
        }
        
        # Mock conversion failure
        with patch.object(service, "_convert_video_to_audio") as mock_convert:
            mock_convert.side_effect = ConversionError("Failed to convert video")
            
            # Call the method and expect an exception
            with pytest.raises(ConversionError):
                service.extract_audio_from_video(sample_video_file)
                
    def test_extract_audio_storage_error(self, audio_extraction_service, sample_video_file):
        """Test handling of storage errors."""
        service, storage_mock = audio_extraction_service
        
        # Mock file metadata
        storage_mock.get_file_metadata.return_value = {
            "filename": sample_video_file,
            "content_type": "video/mp4",
            "size": 1024
        }
        
        # Mock storage failure
        storage_mock.get_file_metadata.side_effect = StorageError("Failed to access storage")
        
        # Call the method and expect an exception
        with pytest.raises(StorageError):
            service.extract_audio_from_video(sample_video_file)
            
    def test_get_extraction_status(self, audio_extraction_service, sample_extraction_result):
        """Test retrieving extraction job status."""
        service, storage_mock = audio_extraction_service
        
        job_id = sample_extraction_result.job_id
        
        # Mock retrieval of job status
        storage_mock.get_extraction_job.return_value = sample_extraction_result
        
        # Call the method under test
        result = service.get_extraction_status(job_id)
        
        # Assertions
        assert result is not None
        assert result.job_id == job_id
        assert result.status == ProcessingStatus.COMPLETED
        assert storage_mock.get_extraction_job.called_with(job_id)
    
    def test_clean_up_old_files(self, audio_extraction_service):
        """Test cleaning up old files."""
        service, storage_mock = audio_extraction_service
        
        # Mock list of old files
        storage_mock.list_old_files.return_value = ["file1.mp4", "file2.mp4"]
        
        # Call the method under test
        service.clean_up_old_files()
        
        # Assertions
        assert storage_mock.list_old_files.called
        assert storage_mock.delete_file.call_count == 2