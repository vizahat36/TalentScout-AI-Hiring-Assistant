"""
Input validation utilities
"""
import re

def validate_input(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """
    Validate user input text
    
    Args:
        text: Input text to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
    
    Returns:
        True if valid, False otherwise
    """
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    
    if len(text) < min_length or len(text) > max_length:
        return False
    
    return True

def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid phone format, False otherwise
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]+', '', phone)
    
    # Check if it's digits and reasonable length
    return cleaned.isdigit() and 10 <= len(cleaned) <= 15

def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters
    
    Args:
        text: Input text to sanitize
    
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove any HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text.strip()

def validate_name(name: str) -> bool:
    """
    Validate candidate name
    
    Args:
        name: Name to validate
    
    Returns:
        True if valid name, False otherwise
    """
    if not validate_input(name, min_length=2, max_length=100):
        return False
    
    # Allow letters, spaces, hyphens, and apostrophes
    pattern = r"^[a-zA-Z\s\-']+$"
    return bool(re.match(pattern, name))
