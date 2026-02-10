import os
import streamlit as st
import json
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables for local development access
load_dotenv()

class NetworkAdvisor:
    """
    Brain Module: Analyzes career context to recommend LinkedIn industry leaders using Groq.
    Supports multilingual output (English, Arabic, French).
    """
    
    def __init__(self):
        # 1. Initialize attributes to None to avoid "no attribute 'client'" errors
        self.client = None
        self.api_key = None
        self.model = "llama-3.3-70b-versatile"

        # 2. Securely fetch the API key with fallback logic (Cloud -> Local)
        try:
            # Attempt to pull from Streamlit Cloud Secrets
            if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                self.api_key = st.secrets["GROQ_API_KEY"]
            else:
                # Fallback to local .env variable
                self.api_key = os.getenv("GROQ_API_KEY")
        except Exception:
            # Final fallback to os.getenv if st.secrets is unavailable locally
            self.api_key = os.getenv("GROQ_API_KEY")

        # 3. Validate key existence
        if not self.api_key:
            raise ValueError("CRITICAL: GROQ_API_KEY is missing. Add it to .env (local) or Secrets (cloud).")

        # 4. Initialize the Groq-powered OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def get_recommendations(self, profile_text: str) -> dict:
        """
        Processes career context and returns 3 real LinkedIn influencers in a structured JSON.
        """
        # Safety check to ensure client is initialized
        if not self.client:
            return {"error": "AI Client not initialized. Please check your API Key."}

        if not profile_text.strip():
            return {"error": "No input provided for analysis."}

        # System instructions for personality and strict JSON output
        system_msg = (
            "You are a LinkedIn Networking Expert. Detect the input language "
            "and provide 3 real influential people to follow in that SAME language. "
            "Return ONLY a valid JSON object."
        )
        
        # Structured prompt for consistent JSON schema
        user_msg = f"""
        Analyze the following career context and suggest 3 LinkedIn influencers:
        ---
        {profile_text}
        ---
        Required JSON Format:
        {{
            "target_niche": "Career Field Name",
            "recommendations": [
                "Name | Profile_URL | Brief Reason to Follow",
                "Name | Profile_URL | Brief Reason to Follow",
                "Name | Profile_URL | Brief Reason to Follow"
            ]
        }}
        """

        try:
            # Execute inference with JSON mode enabled
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the JSON string into a dictionary
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            # Graceful fallback error reporting
            return {"error": f"Groq Networking Module failed: {str(e)}"}

if __name__ == "__main__":
    # Sanity check for module initialization
    print("NetworkAdvisor Brain Module initialized with Groq (Llama 70B).")