import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

class SkillAdvisor:
    """Analyzes skill gaps and provides career development advice using Groq Llama models."""
    
    def __init__(self):
        # Securely fetch Groq API key from environment
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing in .env")
        
        # Pointing to Groq API instead of OpenAI
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Llama 3.3 70B is highly capable of structured reasoning and roadmaps
        self.model = "llama-3.3-70b-versatile"

    def analyze_skills(self, current_skills: str, target_role: str, language: str) -> dict:
        """
        Compares current skills with a target job role and suggests missing skills.
        Supports English, Arabic, and French.
        """
        
        system_msg = (
            f"You are a Career Path Advisor. Analyze the user's skills for the role of {target_role}. "
            f"Respond in {language}. Return ONLY a valid JSON object."
        )
        
        user_msg = f"""
        Target Role: {target_role}
        My Current Skills: {current_skills}
        
        Please provide:
        1. A gap analysis (what is missing).
        2. Top 3 technical skills to learn.
        3. Top 2 soft skills to improve.
        4. A 3-month roadmap summary.
        
        Return JSON with keys: gap_analysis, tech_skills, soft_skills, roadmap.
        """

        try:
            # API call to Groq model with JSON response format
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
            return {"error": f"Skill analysis failed via Groq: {str(e)}"}

if __name__ == "__main__":
    # Internal module test
    print("SkillAdvisor module ready with Groq (Llama 70B).")