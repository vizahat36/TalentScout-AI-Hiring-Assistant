"""
Configuration settings for TalentScout AI Hiring Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
MODEL_NAME = "gpt-4o-mini"
GEMINI_MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.7

# LLM Provider Selection (use 'openai' or 'gemini')
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

# Application Settings
APP_NAME = "TalentScout AI Hiring Assistant"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Data paths
DATA_DIR = "data"
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.json")
