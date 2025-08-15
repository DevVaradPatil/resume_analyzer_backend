class ApiError(Exception):
    """Base API Exception class for custom error handling"""
    status_code = 500
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """Convert exception to dict for JSON response"""
        rv = {
            'status': 'error',
            'error': self.message
        }
        if self.payload:
            rv['payload'] = self.payload
        return rv

class BadRequestError(ApiError):
    """Exception for 400 Bad Request errors"""
    def __init__(self, message, payload=None):
        super().__init__(message, 400, payload)

class NotFoundError(ApiError):
    """Exception for 404 Not Found errors"""
    def __init__(self, message, payload=None):
        super().__init__(message, 404, payload)

class ValidationError(ApiError):
    """Exception for validation errors"""
    def __init__(self, message, payload=None):
        super().__init__(message, 422, payload)

class ServerError(ApiError):
    """Exception for 500 Server errors"""
    def __init__(self, message, payload=None):
        super().__init__(message, 500, payload)
