import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables from .env
load_dotenv()

class ProfileAnalyzer:
    """
    Core engine to analyze LinkedIn profiles using Groq Llama models.
    Supports English, Arabic, and French.
    """
    
    def __init__(self):
        # Securely get the Groq API key
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("CRITICAL ERROR: GROQ_API_KEY is not set in .env file.")
        
        # Pointing the client to Groq's infrastructure
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Using Llama 3.3 70B for high-quality professional analysis
        self.model = "llama-3.3-70b-versatile"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def analyze_profile(self, profile_text: str) -> dict:
        """
        Processes the profile text and returns a structured JSON report.
        The response language will match the input language automatically.
        """
        if not profile_text.strip():
            return {"error": "Input text is empty. Please provide profile content."}

        # System instructions to ensure multilingual support and JSON format
        system_msg = (
            "You are an expert LinkedIn Profile Auditor and Career Coach. "
            "You must detect the language of the input (English, Arabic, or French) "
            "and provide the entire analysis in that SAME language. "
            "Return ONLY a valid JSON object."
        )
        
        user_msg = f"""
        Analyze the following LinkedIn profile content:
        ---
        {profile_text}
        ---
        Provide a comprehensive report in JSON format with these exact keys:
        1. "score": (Integer between 0-100)
        2. "summary": (A brief professional overview)
        3. "strengths": (A list of 3 key strengths found)
        4. "weaknesses": (A list of 3 areas for improvement)
        5. "actionable_tips": (A list of 3 specific steps to boost profile visibility)
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
            
            # Parse the string response into a Python dictionary
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            # Handle API-specific errors (like rate limits or quota)
            return {"error": f"Groq Analysis failed: {str(e)}"}

if __name__ == "__main__":
    # Internal module test
    print("ProfileAnalyzer module ready with Groq integration.")