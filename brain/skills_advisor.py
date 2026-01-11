import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

class SkillAdvisor:
    """Analyzes skill gaps and provides career development advice."""
    
    def __init__(self):
        # Securely fetch API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is missing in .env")
        
        self.client = OpenAI(api_key=self.api_key)

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
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Skill analysis failed: {str(e)}"}