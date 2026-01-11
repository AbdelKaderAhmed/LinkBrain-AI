import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load keys from .env file
load_dotenv()

class ProfileAnalyzer:
    """Class to handle the AI analysis of LinkedIn profiles."""
    
    def __init__(self):
        # Retrieve the API Key from environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("ERROR: OPENAI_API_KEY is missing in .env")
        
        # Initialize OpenAI Client
        self.client = OpenAI(api_key=self.api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def analyze_profile(self, profile_text: str) -> dict:
        """
        Analyzes profile content and returns a JSON report.
        Includes retry logic to handle API timeouts or errors.
        """
        if not profile_text.strip():
            return {"error": "The input text is empty. Please provide content."}

        # The prompt defines how the AI should behave
        system_prompt = "You are an expert LinkedIn Optimizer. Analyze the profile and return ONLY a valid JSON object."
        user_prompt = f"Analyze this LinkedIn profile text. Provide a score (0-100), summary, 3 strengths, 3 weaknesses, and 3 actionable tips:\n\n{profile_text}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Cost-effective and fast
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"} # Guarantees a clean JSON output
            )
            
            # Extract and parse the JSON string from the response
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"AI process failed: {str(e)}"}

# Local Test: This part runs only if you execute this file directly
if __name__ == "__main__":
    print("Testing ProfileAnalyzer logic...")