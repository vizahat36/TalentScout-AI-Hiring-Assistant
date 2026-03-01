"""
Configuration settings for TalentScout AI Hiring Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    
    # Application Settings
    APP_NAME = os.getenv("APP_NAME", "TalentScout AI Hiring Assistant")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Data paths
    DATA_DIR = "data"
    CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
    
    def __init__(self):
        self.validate_settings()
    
    def validate_settings(self):
        """Validate required settings"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in .env file")
    
    def __repr__(self):
        return f"Settings(model={self.MODEL_NAME}, debug={self.DEBUG})"
