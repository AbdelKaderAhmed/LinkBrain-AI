import os
import streamlit as st 
from openai import OpenAI
from dotenv import load_dotenv

# Initialize environment variables for local development
load_dotenv()

class PostGenerator:
    """
    Handles LinkedIn content generation using Groq Llama models.
    Supports high-quality generation in English, Arabic, and French.
    """
    
    def __init__(self):
        # 1. Initialize attributes to None to avoid "AttributeError"
        self.client = None
        self.api_key = None
        self.model = "llama-3.3-70b-versatile"
        
        # 2. Securely fetch the API key with fallback logic
        try:
            # Check for Streamlit Cloud Secrets
            if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                self.api_key = st.secrets["GROQ_API_KEY"]
            else:
                # Local fallback
                self.api_key = os.getenv("GROQ_API_KEY")
        except Exception:
            # Final fallback to environment variables
            self.api_key = os.getenv("GROQ_API_KEY")

        # 3. Validate API key presence
        if not self.api_key:
            raise ValueError("CRITICAL: GROQ_API_KEY is missing. Add it to .env (local) or Secrets (cloud).")

        # 4. Initialize the Groq-powered client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def generate_post(self, topic: str, tone: str, language: str) -> str:
        """
        Creates a LinkedIn post based on topic, tone, and language.
        """
        # Safety check: ensure AI client is initialized
        if not self.client:
            return "Content generation unavailable. Please check API configuration."

        # Define system behavior based on user-selected language and tone
        system_msg = (
            f"You are a professional LinkedIn Content Strategist. "
            f"Write a high-quality post in {language}. The tone must be {tone}. "
            f"Use emojis, professional formatting, and clear bullet points."
        )
        
        user_msg = f"Write a LinkedIn post about the following topic: {topic}. Include 3-5 relevant hashtags."

        try:
            # API call to Groq infrastructure
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.7 # Slight increase in temperature for creative writing
            )
            # Extract and return the generated text content
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during post generation: {str(e)}"

if __name__ == "__main__":
    # Internal module sanity check
    print("PostGenerator module ready with Groq integration.")