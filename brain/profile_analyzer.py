import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

class ProfileAnalyzer:
    """Analyzes LinkedIn profiles using OpenAI models with professional clean code."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key missing! Please check your .env file.")
        self.client = OpenAI(api_key=self.api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def analyze_profile(self, text: str) -> dict:
        """Sends profile text to OpenAI and returns a structured JSON report."""
        if not text.strip():
            return {"error": "Input text is empty."}

        # Clear English comments for logic
        # Sending request to GPT-4o-mini for cost-effective analysis
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert LinkedIn Career Coach. Return JSON only."},
                {"role": "user", "content": f"Analyze this profile and score it (0-100). Provide strengths, weaknesses, and 3 tips:\n\n{text}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    # Quick local test
    print("Testing ProfileAnalyzer...")