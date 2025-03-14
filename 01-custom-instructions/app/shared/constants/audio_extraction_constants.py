"""
Constants for the audio extraction feature.
"""
from typing import Dict, List, Set

# File types
SUPPORTED_VIDEO_FORMATS: Set[str] = {"mp4", "avi", "mov", "wmv", "mkv", "flv"}
AUDIO_OUTPUT_FORMAT: str = "mp3"

# File size limits (in bytes)
MAX_FILE_SIZE: int = 2 * 1024 * 1024 * 1024  # 2GB

# Storage paths
UPLOAD_DIRECTORY: str = "uploads"
PROCESSED_DIRECTORY: str = "processed"
TEMP_DIRECTORY: str = "temp"

# Audio conversion settings
AUDIO_CONVERSION_SETTINGS: Dict[str, str] = {
    "codec": "libmp3lame",
    "bitrate": "192k",
    "sample_rate": "44100",
    "channels": "1",  # Mono channel
}

# Cleanup settings
CLEANUP_THRESHOLD_MINUTES: int = 30  # Files older than this will be deleted during cleanup