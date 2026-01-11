import os
from openai import OpenAI
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

class PostGenerator:
    """Handles LinkedIn content generation using OpenAI models."""
    
    def __init__(self):
        # Securely fetch API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured in .env")
        
        self.client = OpenAI(api_key=self.api_key)

    def generate_post(self, topic: str, tone: str, language: str) -> str:
        """
        Creates a LinkedIn post based on topic, tone, and language.
        Supports English, Arabic, and French.
        """
        
        # System instructions for the AI model
        system_msg = (
            f"You are a professional LinkedIn Content Strategist. "
            f"Write a high-quality post in {language}. The tone must be {tone}. "
            f"Use emojis, professional formatting, and clear bullet points."
        )
        
        user_msg = f"Write a LinkedIn post about the following topic: {topic}. Include 3-5 relevant hashtags."

        try:
            # API call to OpenAI GPT model
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ]
            )
            # Return the generated content string
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during post generation: {str(e)}"