import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load local environment variables (used for local development only)
load_dotenv()

class ProfileAnalyzer:
    """
    Core engine to analyze LinkedIn profiles using Groq Llama models.
    Supports English, Arabic, and French.
    """
    
    def __init__(self):
        # 1. Initialize attributes to None to avoid "AttributeError"
        self.client = None
        self.api_key = None
        self.model = "llama-3.3-70b-versatile"
        
        # 2. Securely fetch the API key with fallback logic
        try:
            # Check if running on Streamlit Cloud (st.secrets)
            if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                self.api_key = st.secrets["GROQ_API_KEY"]
            else:
                # Fallback to local environment variable
                self.api_key = os.getenv("GROQ_API_KEY")
        except Exception:
            # Final fallback to os.getenv if st.secrets triggers an error locally
            self.api_key = os.getenv("GROQ_API_KEY")

        # 3. Validate API key existence before initializing the client
        if not self.api_key:
            raise ValueError("CRITICAL ERROR: GROQ_API_KEY is not set in Secrets or .env file.")
        
        # 4. Initialize the OpenAI client pointing to Groq's infrastructure
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def analyze_profile(self, profile_text: str) -> dict:
        """
        Processes profile text and returns a structured JSON report.
        Response language will match input language (Multilingual support).
        """
        # Ensure the client was successfully initialized
        if not self.client:
            return {"error": "AI Client not initialized. Please check your API Key configuration."}
            
        if not profile_text.strip():
            return {"error": "Input text is empty. Please provide profile content."}

        # System instructions for behavior and output format
        system_msg = (
            "You are an expert LinkedIn Profile Auditor and Career Coach. "
            "Detect the input language (English, Arabic, or French) "
            "and provide the analysis in that SAME language. "
            "Return ONLY a valid JSON object."
        )
        
        user_msg = f"""
        Analyze the following LinkedIn profile content:
        ---
        {profile_text}
        ---
        Provide a report in JSON format with these exact keys:
        1. "score": (Integer 0-100)
        2. "summary": (Professional overview)
        3. "strengths": (List of 3 key strengths)
        4. "weaknesses": (List of 3 improvement areas)
        5. "actionable_tips": (List of 3 specific steps)
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse and return the JSON response
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            # Handle API-specific errors
            return {"error": f"Groq Analysis failed: {str(e)}"}

if __name__ == "__main__":
    # Module testing entry point
    print("ProfileAnalyzer module ready with Groq integration.")