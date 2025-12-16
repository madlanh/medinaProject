"""
File Upload Utility Module
Handles file upload, validation, and management for the application.

Features:
- Validates file extensions (jpg, jpeg, png, gif, webp)
- Generates unique filenames using timestamp + UUID
- Saves files to appropriate category directories
- Provides file deletion functionality
"""
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

# Maximum file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


def allowed_file(filename: str) -> bool:
    """
    Check if the file extension is allowed.
    
    Args:
        filename: The name of the file to check
        
    Returns:
        True if extension is allowed, False otherwise
    """
    if not filename:
        return False
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename using timestamp and UUID.
    
    Args:
        original_filename: The original filename
        
    Returns:
        A unique filename with the same extension
    """
    if not original_filename:
        return None
        
    ext = original_filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{unique_id}.{ext}"


def get_upload_path(category: str) -> str:
    """
    Get the full upload path for a category.
    
    Args:
        category: The category folder (e.g., 'banners', 'galeri', 'kepsek')
        
    Returns:
        Full path to the upload directory
    """
    static_folder = current_app.static_folder
    upload_path = os.path.join(static_folder, 'images', category)
    
    # Create directory if it doesn't exist
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    return upload_path


def save_uploaded_file(file, category: str) -> str | None:
    """
    Save an uploaded file to the specified category directory.
    
    Args:
        file: The FileStorage object from Flask request
        category: The category folder (e.g., 'banners', 'galeri', 'kepsek')
        
    Returns:
        The URL path to the saved file, or None if save failed
        
    Raises:
        ValueError: If file is invalid or too large
    """
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        raise ValueError(f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB")
    
    # Generate unique filename
    filename = generate_unique_filename(secure_filename(file.filename))
    if not filename:
        return None
    
    # Get upload path and save
    upload_path = get_upload_path(category)
    file_path = os.path.join(upload_path, filename)
    
    try:
        file.save(file_path)
        # Return URL path relative to static folder
        return f"/static/images/{category}/{filename}"
    except Exception as e:
        current_app.logger.error(f"Failed to save file: {e}")
        return None


def delete_file(file_url: str) -> bool:
    """
    Delete a file from the filesystem.
    
    Args:
        file_url: The URL path to the file (e.g., '/static/images/galeri/photo.jpg')
        
    Returns:
        True if file was deleted, False otherwise
    """
    if not file_url or not file_url.startswith('/static/'):
        return False
    
    # Convert URL to filesystem path
    relative_path = file_url.replace('/static/', '')
    static_folder = current_app.static_folder
    file_path = os.path.join(static_folder, relative_path)
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"Failed to delete file: {e}")
        return False
