import os
from app import app
from config import get_config

def init_app():
    """Initialize the application with proper configuration"""
    config = get_config()
    
    # Create upload folder if it doesn't exist
    if not os.path.exists(config.UPLOAD_FOLDER):
        os.makedirs(config.UPLOAD_FOLDER)
    
    # Apply configuration to app
    app.config.from_object(config)
    
    # Clean up old files in uploads directory
    try:
        from utils.file_management import cleanup_old_files
        cleanup_old_files(config.UPLOAD_FOLDER, max_age_hours=24)
    except Exception as e:
        print(f"Error cleaning up files: {e}")
    
    return app

if __name__ == "__main__":
    app = init_app()
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host='0.0.0.0', port=port)
