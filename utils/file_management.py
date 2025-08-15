"""
Utility functions for file management
"""
import os
import time
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def cleanup_old_files(directory, max_age_hours=24):
    """
    Delete files in the specified directory that are older than the maximum age
    
    Args:
        directory (str): Path to the directory to clean
        max_age_hours (int): Maximum age of files in hours before deletion
    
    Returns:
        int: Number of files deleted
    """
    if not os.path.exists(directory):
        logger.warning(f"Directory {directory} does not exist")
        return 0
    
    count = 0
    current_time = time.time()
    max_age = timedelta(hours=max_age_hours).total_seconds()
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Check file age
        file_age = current_time - os.path.getmtime(file_path)
        if file_age > max_age:
            try:
                os.remove(file_path)
                logger.info(f"Deleted old file: {filename}")
                count += 1
            except Exception as e:
                logger.error(f"Error deleting file {filename}: {e}")
    
    return count
