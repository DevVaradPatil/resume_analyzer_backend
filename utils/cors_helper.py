"""
CORS helper utilities for consistent CORS handling
"""
import os
from flask import request, make_response

def get_cors_origins():
    """
    Get allowed origins from environment variable or use defaults
    
    Returns:
        list: List of allowed origins
    """
    return os.getenv('CORS_ORIGINS', 'http://localhost:5173,https://resumeanalyzer-alpha.vercel.app').split(',')

def add_cors_headers(response):
    """
    Add CORS headers to a response
    
    Args:
        response: Flask response object
    
    Returns:
        response: Flask response with CORS headers
    """
    cors_origins = get_cors_origins()
    origin = request.headers.get('Origin', '')
    
    # If origin is in the allowed list, set it specifically (better for credentials)
    # Otherwise, don't set the header at all
    if origin in cors_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
    
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
    
    return response

def cors_preflight_response():
    """
    Create a response for CORS preflight requests
    
    Returns:
        response: Flask response for preflight request
    """
    response = make_response()
    return add_cors_headers(response)
