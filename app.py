"""
TalentScout AI Hiring Assistant - Main Application
"""
from config.settings import Settings
from services.conversation_manager import ConversationManager
from services.data_handler import DataHandler
from utils.validators import validate_input

def main():
    """Main application entry point"""
    print("=" * 60)
    print("Welcome to TalentScout AI Hiring Assistant")
    print("=" * 60)
    
    # Initialize services
    settings = Settings()
    conversation_manager = ConversationManager()
    data_handler = DataHandler()
    
    # Start the interview process
    conversation_manager.start_interview()

if __name__ == "__main__":
    main()
