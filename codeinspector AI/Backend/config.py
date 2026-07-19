import os
from datetime import timedelta

class Config:
    # Application security keys
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my-super-secret-key-123')
    
    # Humaray project ka main database (SQLite for development)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///code_review.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT authentication settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-me')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    
    # File upload handling directories
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')