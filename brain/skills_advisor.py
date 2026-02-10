import os
import streamlit as st
import json
from openai import OpenAI
from dotenv import load_dotenv

# Initialize environment variables for local development access
load_dotenv()

class SkillAdvisor:
    """
    Analyzes skill gaps and provides career development advice using Groq Llama models.
    Supports English, Arabic, and French.
    """
    
    def __init__(self):
        # 1. Initialize attributes to None to prevent "no attribute 'client'" errors
        self.client = None
        self.api_key = None
        self.model = "llama-3.3-70b-versatile"

        # 2. Securely fetch the API key with fallback logic (Cloud -> Local)
        try:
            # Check if running on Streamlit Cloud (using Secrets)
            if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                self.api_key = st.secrets["GROQ_API_KEY"]
            else:
                # Fallback to local .env environment variable
                self.api_key = os.getenv("GROQ_API_KEY")
        except Exception:
            # Final fallback to os.getenv if st.secrets triggers an error locally
            self.api_key = os.getenv("GROQ_API_KEY")

        # 3. Validate key existence before proceeding
        if not self.api_key:
            raise ValueError("CRITICAL: GROQ_API_KEY is missing. Add it to .env (local) or Secrets (cloud).")

        # 4. Initialize the OpenAI client pointing to Groq's API
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def analyze_skills(self, current_skills: str, target_role: str, language: str) -> dict:
        """
        Compares current skills with a target job role and suggests missing skills.
        Returns a structured JSON object.
        """
        # Safety check: ensure the AI client was initialized correctly
        if not self.client:
            return {"error": "AI Client not initialized. Please check system configuration."}
        
        # System personality and instruction for strict JSON output
        system_msg = (
            f"You are a Career Path Advisor. Analyze the user's skills for the role of {target_role}. "
            f"Respond in {language}. Return ONLY a valid JSON object."
        )
        
        # Structured user query for the model
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
            # Execute API call with JSON mode enabled
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the text response into a Python dictionary
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            # Professional fallback error reporting
            return {"error": f"Skill analysis failed via Groq: {str(e)}"}

if __name__ == "__main__":
    # Module testing entry point
    print("SkillAdvisor module ready with Groq (Llama 70B).")