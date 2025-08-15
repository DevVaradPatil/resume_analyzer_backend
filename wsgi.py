"""
WSGI entry point for production servers like Gunicorn or uWSGI
"""
from run import init_app

# Initialize the application
application = init_app()

# For compatibility with some WSGI servers that look for 'app'
app = application

if __name__ == "__main__":
    application.run()
