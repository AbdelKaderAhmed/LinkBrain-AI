import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables for API access
load_dotenv()

class NetworkAdvisor:
    """
    Brain Module: Analyzes career context to recommend LinkedIn industry leaders.
    """
    
    def __init__(self):
        # Securely initialize OpenAI client
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key missing: Ensure OPENAI_API_KEY is in .env")
        
        self.client = OpenAI(api_key=self.api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def get_recommendations(self, profile_text: str) -> dict:
        """
        Detects language and returns 3 LinkedIn influencers in a structured JSON.
        """
        if not profile_text.strip():
            return {"error": "No input provided."}

        # System instructions for language detection and formatting
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
            # Call OpenAI Chat Completion
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse and return JSON data
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Brain module failed to process networking: {str(e)}"}

if __name__ == "__main__":
    # Internal component check
    print("NetworkAdvisor Brain Module initialized.")