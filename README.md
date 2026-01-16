# 🧠 LinkBrain AI | Career Intelligence Hub

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://linkbrain-ai.streamlit.app/)

> **Elevate your career with AI-powered insights.** > [🚀 View Live Demo](https://linkbrain-ai.streamlit.app/) | [📁 Source Code](https://github.com/AbdelKaderAhmed/LinkBrain-AI)

**LinkBrain AI** is an AI-powered suite designed to maximize your professional impact. 

- 🤖 **AI Coach:** Context-aware guidance based on your data.
- 🔍 **Audit:** Deep LinkedIn profile & SWOT analysis.
- 🛤️ **Growth:** Actionable skill roadmaps & networking.

---

## 🚀 Key Features

* **🔍 Profile Optimizer:** Deep audit of LinkedIn profiles with a professional score, summary, and SWOT analysis (Strengths/Weaknesses).
* **✍️ AI Content Creator:** Generates high-engagement LinkedIn posts based on specific topics, tones (Storytelling, Professional, Educational), and languages.
* **📊 Market Skill Advisor:** Analyzes the gap between your current skills and a target job role to provide a 3-month learning roadmap.
* **🌐 Networking Advisor:** Identifies and recommends industry leaders and influencers to follow for strategic career growth.
* **💬 Strategic AI Concierge:** A context-aware chatbot that uses your specific profile data to provide real-time career coaching.
* **📦 Master Career Bundle:** A unique feature that compiles all your analyses into a single, branded PDF report.


## 📂 Project Structure
```text
├── app.py                # Main Application & Professional UI
├── logo.png              # Brand Asset
├── .env                  # Environment Variables (Secure API Keys)
├── requirements.txt      # Dependency Manifest
│
├── brain/                # AI Logic Core
│   ├── career_coach.py     # Personalized Mentor Logic
│   ├── post_generator.py   # Content Creation Engine
│   ├── profile_analyzer.py # SWOT & Audit Analysis
│   └── skills_advisor.py   # Roadmap & Gap Logic
│
└── utils/                # Supporting Utilities
    ├── __init__.py       # Package-level exposure for cleaner imports
    └── pdf_exporter.py     # Document Generation Engine



---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Engine:** [OpenAI GPT-4o-mini](https://openai.com/)
- **Backend Logic:** Python 3.x
- **PDF Generation:** FPDF
- **Environment Management:** Python-Dotenv

---

⚙️ Installation & Deployment

 1.Clone the project:
 git clone https://github.com/AbdelKaderAhmed/LinkBrain-AI.git
 cd LinkBrain-AI

2.Setup environment:
pip install -r requirements.txt

3.Configure API Key: Add your OPENAI_API_KEY to a .env file in the root directory.

4.Run the Dashboard:
streamlit run app.py


👨‍💻 Developer
Abdel Kader Ahmed Junior AI Engineer 
