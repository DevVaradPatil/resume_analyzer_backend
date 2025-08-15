from flask import Flask, jsonify
from flask_cors import CORS
from routes import api
from utils.errors import ApiError

def create_app():
    """
    Create and configure the Flask application
    
    Returns:
        Flask: The configured Flask application
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api)
    
    # Register error handlers
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "error": "The requested resource was not found"
        }), 404
        
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "status": "error",
            "error": "The method is not allowed for this resource"
        }), 405
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "status": "error",
            "error": "Internal server error"
        }), 500
    
    return app

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
