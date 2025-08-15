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
    
    return app

if __name__ == "__main__":
    app = init_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
