"""
Gemini LLM service for technical question generation.

This service provides an alternative to OpenAI using Google's Gemini API.
"""
import warnings
from typing import Any
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, TEMPERATURE

try:
    from google import genai as google_genai_new
    HAS_NEW_GENAI = True
except Exception:
    HAS_NEW_GENAI = False
    google_genai_new = None

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        import google.generativeai as google_genai_old
    HAS_OLD_GENAI = True
except Exception:
    HAS_OLD_GENAI = False
    google_genai_old = None


class GeminiService:
    """
    GeminiService handles interactions with Google's Gemini model.
    Provides same interface as LLMService for easy switching.
    """

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not found. Please set it in .env file.")

        if HAS_NEW_GENAI:
            if google_genai_new is None:
                raise ImportError("google.genai import failed.")
            self.provider = "new"
            self.client = google_genai_new.Client(api_key=GEMINI_API_KEY)
        elif HAS_OLD_GENAI:
            if google_genai_old is None:
                raise ImportError("google.generativeai import failed.")
            self.provider = "old"
            configure_fn = getattr(google_genai_old, "configure")
            configure_fn(api_key=GEMINI_API_KEY)
            model_name = GEMINI_MODEL if GEMINI_MODEL.startswith("models/") else f"models/{GEMINI_MODEL}"
            model_cls = getattr(google_genai_old, "GenerativeModel")
            self.model = model_cls(model_name)
        else:
            raise ImportError(
                "No Gemini SDK found. Install `google-genai` (preferred) or `google-generativeai`."
            )

    def generate_response(self, messages: list) -> str:
        """
        Generate response using Gemini model.
        
        Converts OpenAI-style messages format to Gemini format.
        
        :param messages: List of message dictionaries (OpenAI format)
        :return: Model response as string
        """
        try:
            # Convert OpenAI messages format to Gemini prompt
            prompt = self._convert_messages_to_prompt(messages)

            if self.provider == "new":
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config={
                        "temperature": TEMPERATURE,
                        "max_output_tokens": 2048,
                    },
                )
                return (response.text or "").strip()

            generation_config: Any = {
                "temperature": TEMPERATURE,
                "max_output_tokens": 2048,
            }
            response = self.model.generate_content(prompt, generation_config=generation_config)
            return (response.text or "").strip()

        except Exception as e:
            print(f"Gemini Error: {e}")
            return "I'm experiencing technical difficulties. Please try again later."

    def _convert_messages_to_prompt(self, messages: list) -> str:
        """
        Convert OpenAI messages format to a single prompt string for Gemini.
        
        :param messages: List of message dicts with 'role' and 'content'
        :return: Combined prompt string
        """
        prompt_parts = []
        
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"Instructions: {content}\n")
            elif role == "user":
                prompt_parts.append(f"Request: {content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Response: {content}\n")
        
        return "\n".join(prompt_parts)
