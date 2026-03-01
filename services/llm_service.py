"""
LLM Service for handling OpenAI API interactions
"""
import openai
from config.settings import Settings
from utils.fallback import handle_api_error

class LLMService:
    """Service for interacting with OpenAI's LLM"""
    
    def __init__(self):
        self.settings = Settings()
        openai.api_key = self.settings.OPENAI_API_KEY
        self.model = self.settings.MODEL_NAME
        self.temperature = self.settings.TEMPERATURE
        self.max_tokens = self.settings.MAX_TOKENS
    
    def generate_response(self, messages: list, **kwargs) -> str:
        """
        Generate a response from the LLM
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional parameters for the API call
        
        Returns:
            Generated response text
        """
        try:
            response = openai.ChatCompletion.create(
                model=kwargs.get('model', self.model),
                messages=messages,
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens)
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return handle_api_error(e)
    
    def generate_interview_question(self, context: dict) -> str:
        """Generate an interview question based on context"""
        messages = [
            {"role": "system", "content": "You are generating interview questions."},
            {"role": "user", "content": f"Generate a question for: {context}"}
        ]
        return self.generate_response(messages)
    
    def evaluate_response(self, question: str, answer: str) -> dict:
        """Evaluate a candidate's response"""
        messages = [
            {"role": "system", "content": "You are evaluating interview responses."},
            {"role": "user", "content": f"Question: {question}\nAnswer: {answer}\n\nProvide evaluation."}
        ]
        evaluation = self.generate_response(messages)
        return {"evaluation": evaluation}
