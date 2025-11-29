import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
# Default SameSite to "Lax" for localhost http testing. In production, set
# JWT_COOKIE_SAMESITE=None and COOKIE_SECURE=true via environment variables.
JWT_COOKIE_SAMESITE = os.getenv("JWT_COOKIE_SAMESITE", "Lax")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    FRONTEND_ORIGIN = FRONTEND_ORIGIN

    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_COOKIE_SECURE = COOKIE_SECURE
    JWT_COOKIE_SAMESITE = JWT_COOKIE_SAMESITE
    JWT_COOKIE_CSRF_PROTECT = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}