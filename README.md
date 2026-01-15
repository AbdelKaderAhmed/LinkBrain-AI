# 🧠 LinkBrain AI | Career Intelligence Hub

**LinkBrain AI** is a professional-grade career optimization suite designed to help LinkedIn users maximize their professional impact. Powered by OpenAI's GPT-4o-mini, it analyzes profiles, generates engaging content, provides skill roadmaps, and suggests networking strategies.

---

## 🚀 Key Features

* **🔍 Profile Optimizer:** Deep audit of LinkedIn profiles with a professional score, summary, and SWOT analysis (Strengths/Weaknesses).
* **✍️ AI Content Creator:** Generates high-engagement LinkedIn posts based on specific topics, tones (Storytelling, Professional, Educational), and languages.
* **📊 Market Skill Advisor:** Analyzes the gap between your current skills and a target job role to provide a 3-month learning roadmap.
* **🌐 Networking Advisor:** Identifies and recommends industry leaders and influencers to follow for strategic career growth.
* **💬 Strategic AI Concierge:** A context-aware chatbot that uses your specific profile data to provide real-time career coaching.
* **📦 Master Career Bundle:** A unique feature that compiles all your analyses into a single, branded PDF report.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Engine:** [OpenAI GPT-4o-mini](https://openai.com/)
- **Backend Logic:** Python 3.x
- **PDF Generation:** FPDF
- **Environment Management:** Python-Dotenv

---

## 📂 Project Structure

```text
├── app.py                # Main Streamlit application
├── brain/                # AI Logic Modules
│   ├── profile_analyzer.py
│   ├── skills_advisor.py
│   ├── post_generator.py
│   └── network_advisor.py
├── utils/                # Helper Utilities
│   └── pdf_exporter.py   # PDF generation engine
├── logo.png              # App Branding
└── requirements.txt      # Dependencies