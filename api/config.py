"""
Configuration for FastAPI backend
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """API Settings"""
    
    # API Settings
    API_TITLE = "ERP Implementation Assistant API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "AI-powered M3 implementation guidance"
    
    # CORS Settings
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Model Settings
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0"))
    
    # Rate Limiting (future)
    MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
