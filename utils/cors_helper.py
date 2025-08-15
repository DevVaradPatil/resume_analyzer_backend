"""
CORS helper utilities for consistent CORS handling
"""
import os

def get_cors_origins():
    """
    Get allowed origins from environment variable or use defaults
    
    Returns:
        list: List of allowed origins
    """
    return os.getenv('CORS_ORIGINS', 'http://localhost:5173,https://resumeanalyzer-alpha.vercel.app').split(',')
