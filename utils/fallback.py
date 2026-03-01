"""
Fallback handlers for error scenarios
"""
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_api_error(error: Exception) -> str:
    """
    Handle API errors with fallback responses
    
    Args:
        error: The exception that occurred
    
    Returns:
        Fallback response message
    """
    logger.error(f"API Error: {str(error)}")
    
    error_type = type(error).__name__
    
    fallback_messages = {
        "RateLimitError": "I apologize, but we've reached our API rate limit. Please try again in a moment.",
        "APIError": "I'm experiencing technical difficulties. Let me try that again.",
        "Timeout": "The request took too long. Could you please rephrase your response?",
        "AuthenticationError": "There's an authentication issue. Please contact support.",
        "InvalidRequestError": "There was an issue with the request. Please try again.",
    }
    
    fallback = fallback_messages.get(
        error_type,
        "I encountered an unexpected error. Let's continue with the interview."
    )
    
    return fallback

def get_fallback_question(context: str = "") -> str:
    """
    Get a fallback interview question when API fails
    
    Args:
        context: Context for the fallback question
    
    Returns:
        A generic but relevant interview question
    """
    fallback_questions = [
        "Can you tell me about a challenging project you've worked on?",
        "What interests you most about this position?",
        "How do you approach problem-solving in your work?",
        "Can you describe your ideal work environment?",
        "What are your strongest technical skills?",
    ]
    
    import random
    return random.choice(fallback_questions)

def handle_invalid_response() -> str:
    """
    Handle invalid user responses
    
    Returns:
        Message prompting for valid input
    """
    return "I didn't quite catch that. Could you please provide more details?"

def handle_timeout() -> str:
    """
    Handle conversation timeout scenarios
    
    Returns:
        Timeout message
    """
    logger.warning("Conversation timeout occurred")
    return "I notice you might need more time to think. Take your time, and let me know when you're ready."

def log_error(error: Exception, context: str = ""):
    """
    Log errors with context
    
    Args:
        error: The exception to log
        context: Additional context about where the error occurred
    """
    logger.error(f"Error in {context}: {type(error).__name__} - {str(error)}")
