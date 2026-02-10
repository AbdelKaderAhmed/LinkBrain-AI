import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables for API access
load_dotenv()

class NetworkAdvisor:
    """
    Brain Module: Analyzes career context to recommend LinkedIn industry leaders using Groq.
    """
    
    def __init__(self):
        # Securely initialize Groq client via OpenAI SDK
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API Key missing: Ensure GROQ_API_KEY is in .env")
        
        # Pointing to Groq API infrastructure
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Using Llama 3.3 70B for its extensive knowledge of industry leaders
        self.model = "llama-3.3-70b-versatile"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def get_recommendations(self, profile_text: str) -> dict:
        """
        Detects language and returns 3 LinkedIn influencers in a structured JSON.
        Supports English, Arabic, and French.
        """
        if not profile_text.strip():
            return {"error": "No input provided."}

        # System instructions for language detection and JSON formatting
        system_msg = (
            "You are a LinkedIn Networking Expert. Detect the input language "
            "and provide 3 real influential people to follow in that SAME language. "
            "Return ONLY a valid JSON object."
        )
        
        # Structured user prompt for consistent JSON output
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
            # Call Groq Chat Completion with JSON mode enabled
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse and return JSON data as a Python dictionary
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            # Fallback error handling for the brain module
            return {"error": f"Groq Brain module failed to process networking: {str(e)}"}

if __name__ == "__main__":
    # Internal component check
    print("NetworkAdvisor Brain Module initialized with Groq (Llama 70B).")