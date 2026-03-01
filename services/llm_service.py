"""
Create a reusable LLM service class for OpenAI.

Requirements:
- Load API key from config.settings
- Use GPT-4o-mini model
- Create method: generate_response(messages: list) -> str
- Handle exceptions safely
- Return only clean text response
- Add proper docstrings
- Follow clean architecture principles
"""
from openai import OpenAI
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE


class LLMService:
    """
    LLMService handles all interactions with the OpenAI model.
    It abstracts API calls and provides a clean interface
    for generating responses.
    """

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found. Please set it in .env file.")

        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_response(self, messages: list) -> str:
        """
        Sends structured conversation messages to the OpenAI model
        and returns the generated response text.

        :param messages: List of message dictionaries in OpenAI format
        :return: Model response as string
        """
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=TEMPERATURE
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"LLM Error: {e}")
            return "I'm experiencing technical difficulties. Please try again later."
