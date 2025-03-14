"""
Service for handling storage operations for files.
"""
import os
import shutil
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import mimetypes
from pathlib import Path

from app.shared.exceptions.audio_extraction_exceptions import StorageError
from app.shared.constants.audio_extraction_constants import (
    UPLOAD_DIRECTORY, 
    PROCESSED_DIRECTORY, 
    TEMP_DIRECTORY,
    CLEANUP_THRESHOLD_MINUTES
)


class StorageService:
    """Service for handling file storage operations."""
    
    def __init__(self, base_directory: str = "storage"):
        """
        Initialize the storage service.
        
        Args:
            base_directory: The root directory for all storage operations
        """
        self.base_directory = base_directory
        self.upload_directory = os.path.join(base_directory, UPLOAD_DIRECTORY)
        self.processed_directory = os.path.join(base_directory, PROCESSED_DIRECTORY)
        self.temp_directory = os.path.join(base_directory, TEMP_DIRECTORY)
        
        # Create directories if they don't exist
        for directory in [self.upload_directory, self.processed_directory, self.temp_directory]:
            os.makedirs(directory, exist_ok=True)
    
    def save_file(self, file_content: bytes, file_path: str) -> int:
        """
        Save file content to the specified path.
        
        Args:
            file_content: The content of the file to save
            file_path: The path where to save the file
            
        Returns:
            The size of the saved file in bytes
            
        Raises:
            StorageError: If an error occurs while saving the file
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write the file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Return the file size
            return os.path.getsize(file_path)
        except Exception as e:
            raise StorageError(f"Failed to save file: {e}")
    
    def get_file_path(self, file_id: str, directory: str = UPLOAD_DIRECTORY) -> str:
        """
        Get the full path for a file in the specified directory.
        
        Args:
            file_id: The ID of the file
            directory: The directory where the file is stored
            
        Returns:
            The full path to the file
        """
        return os.path.join(self.base_directory, directory, file_id)
    
    def get_file_content(self, file_path: str) -> bytes:
        """
        Get the content of a file.
        
        Args:
            file_path: The path to the file
            
        Returns:
            The content of the file
            
        Raises:
            StorageError: If an error occurs while reading the file
        """
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            raise StorageError(f"Failed to read file: {e}")
    
    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Get metadata for a file.
        
        Args:
            file_path: The path to the file
            
        Returns:
            A dictionary containing file metadata
            
        Raises:
            StorageError: If an error occurs while getting file metadata
        """
        try:
            stat_info = os.stat(file_path)
            filename = os.path.basename(file_path)
            content_type, _ = mimetypes.guess_type(filename)
            
            return {
                "filename": filename,
                "content_type": content_type or "application/octet-stream",
                "size": stat_info.st_size,
                "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat()
            }
        except Exception as e:
            raise StorageError(f"Failed to get file metadata: {e}")
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get the size of a file in bytes.
        
        Args:
            file_path: The path to the file
            
        Returns:
            The size of the file in bytes
            
        Raises:
            StorageError: If an error occurs while getting file size
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            raise StorageError(f"Failed to get file size: {e}")
    
    def delete_file(self, file_path: str) -> None:
        """
        Delete a file.
        
        Args:
            file_path: The path to the file to delete
            
        Raises:
            StorageError: If an error occurs while deleting the file
        """
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            raise StorageError(f"Failed to delete file: {e}")
    
    def move_file(self, source_path: str, destination_path: str) -> str:
        """
        Move a file from source to destination.
        
        Args:
            source_path: The current path of the file
            destination_path: The path to move the file to
            
        Returns:
            The path to the moved file
            
        Raises:
            StorageError: If an error occurs while moving the file
        """
        try:
            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Move the file
            shutil.move(source_path, destination_path)
            
            return destination_path
        except Exception as e:
            raise StorageError(f"Failed to move file: {e}")
    
    def list_old_files(self, directory: str = UPLOAD_DIRECTORY, 
                        threshold_minutes: int = CLEANUP_THRESHOLD_MINUTES) -> List[str]:
        """
        List files older than the specified threshold.
        
        Args:
            directory: The directory to check for old files
            threshold_minutes: Files older than this (in minutes) will be listed
            
        Returns:
            A list of paths to old files
            
        Raises:
            StorageError: If an error occurs while listing files
        """
        try:
            old_files = []
            threshold_time = datetime.now() - timedelta(minutes=threshold_minutes)
            dir_path = os.path.join(self.base_directory, directory)
            
            if not os.path.exists(dir_path):
                return []
                
            for root, _, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mtime < threshold_time:
                        old_files.append(file_path)
            
            return old_files
        except Exception as e:
            raise StorageError(f"Failed to list old files: {e}")
    
    def save_extraction_job(self, job_data: Dict[str, Any]) -> None:
        """
        Save extraction job data to storage.
        
        Args:
            job_data: The job data to save
            
        Raises:
            StorageError: If an error occurs while saving job data
        """
        try:
            job_id = job_data.get("job_id")
            if not job_id:
                raise ValueError("Job ID is required")
                
            job_path = os.path.join(self.processed_directory, job_id, "job.json")
            os.makedirs(os.path.dirname(job_path), exist_ok=True)
            
            with open(job_path, 'w') as f:
                json.dump(job_data, f)
        except Exception as e:
            raise StorageError(f"Failed to save extraction job: {e}")
    
    def get_extraction_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get extraction job data from storage.
        
        Args:
            job_id: The ID of the job
            
        Returns:
            The job data or None if not found
            
        Raises:
            StorageError: If an error occurs while getting job data
        """
        try:
            job_path = os.path.join(self.processed_directory, job_id, "job.json")
            
            if not os.path.exists(job_path):
                return None
                
            with open(job_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise StorageError(f"Failed to get extraction job: {e}")