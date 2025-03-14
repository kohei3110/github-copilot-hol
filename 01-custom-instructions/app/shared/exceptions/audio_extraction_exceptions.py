"""
Custom exceptions for the audio extraction feature.
"""

class InvalidFileTypeError(Exception):
    """Exception raised when an unsupported file type is provided."""
    def __init__(self, file_type: str, message: str = None):
        self.file_type = file_type
        self.message = message or f"File type '{file_type}' is not supported."
        super().__init__(self.message)


class FileSizeLimitExceededError(Exception):
    """Exception raised when the uploaded file exceeds the size limit."""
    def __init__(self, file_size: int, max_size: int, message: str = None):
        self.file_size = file_size
        self.max_size = max_size
        self.message = message or f"File size ({file_size}) exceeds the maximum limit of {max_size} bytes."
        super().__init__(self.message)


class ConversionError(Exception):
    """Exception raised when an error occurs during file conversion."""
    def __init__(self, message: str = None):
        self.message = message or "An error occurred during file conversion."
        super().__init__(self.message)


class StorageError(Exception):
    """Exception raised when an error occurs during storage operations."""
    def __init__(self, message: str = None):
        self.message = message or "An error occurred during storage operation."
        super().__init__(self.message)