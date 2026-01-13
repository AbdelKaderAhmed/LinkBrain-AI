import streamlit as st
from dotenv import load_dotenv
import os

# Import custom modules from the brain folder
from brain.profile_analyzer import ProfileAnalyzer
from brain.post_generator import PostGenerator
from brain.skills_advisor import SkillAdvisor
from brain.network_advisor import NetworkAdvisor

# Import the PDF utility from the utils folder
from utils.pdf_exporter import PDFReport

# Load environment variables
load_dotenv()

# 1. Page Configuration
st.set_page_config(
    page_title="LinkBrain AI | Career Intelligent Hub",
    page_icon="🧠",
    layout="wide"
)

# 2. Initialize Session State for Master Report
# This keeps data alive when switching between sidebar menu options
if 'master_data' not in st.session_state:
    st.session_state['master_data'] = {
        'profile': None,
        'roadmap': None,
        'networking': None,
        'role': ""
    }

# 3. Global Styling (CSS)
st.markdown("""
    <style>
    .rtl-text { direction: rtl; text-align: right; font-family: 'Tahoma', sans-serif; }
    .main-title { text-align: center; color: #0A66C2; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #0A66C2; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar Navigation
st.sidebar.markdown("<h2 style='text-align: center;'>🧠 LinkBrain Menu</h2>", unsafe_allow_html=True)
app_mode = st.sidebar.selectbox("Select a Tool:", 
    ["Profile Optimizer", "Post Generator", "Skill Advisor", "Networking Recommendations"]
)

# --- FEATURE 1: PROFILE OPTIMIZER ---
if app_mode == "Profile Optimizer":
    st.markdown("<h1 class='main-title'>🔍 LinkedIn Profile Optimizer</h1>", unsafe_allow_html=True)
    profile_input = st.text_area("Paste your profile text here:", height=250)
    
    if st.button("Analyze My Profile"):
        if profile_input:
            with st.spinner("Analyzing..."):
                analyzer = ProfileAnalyzer()
                result = analyzer.analyze_profile(profile_input)
                if "error" in result:
                    st.error(result["error"])
                else:
                    # Save to Session State for Master Report
                    st.session_state['master_data']['profile'] = result
                    st.success("Analysis Complete!")
                    st.metric("Profile Score", f"{result['score']}/100")
                    st.write(result['summary'])
        else:
            st.warning("Please provide profile text.")

# --- FEATURE 2: POST GENERATOR ---
elif app_mode == "Post Generator":
    st.markdown("<h1 class='main-title'>✍️ AI Content Creator</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Post Topic:")
        language = st.selectbox("Language:", ["English", "Arabic", "French"])
    with col2:
        tone = st.selectbox("Tone:", ["Professional", "Storytelling", "Educational"])
    
    if st.button("Generate Post ✨"):
        if topic:
            with st.spinner("Writing..."):
                gen = PostGenerator()
                post_content = gen.generate_post(topic, tone, language)
                dir_class = "rtl-text" if language == "Arabic" else ""
                st.markdown(f'<div class="{dir_class}">{post_content}</div>', unsafe_allow_html=True)

# --- FEATURE 3: SKILL ADVISOR ---
elif app_mode == "Skill Advisor":
    st.markdown("<h1 class='main-title'>📊 Market Skill Advisor</h1>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        role = st.text_input("Target Job Role:")
    with col_b:
        lang = st.selectbox("Language:", ["English", "Arabic", "French"])
    skills_input = st.text_area("Your Current Skills:")

    if st.button("Get Career Roadmap 🚀"):
        if role and skills_input:
            with st.spinner("Generating roadmap..."):
                advisor = SkillAdvisor()
                report = advisor.analyze_skills(skills_input, role, lang)
                if "error" in report:
                    st.error(report["error"])
                else:
                    # Save to Session State for Master Report
                    st.session_state['master_data']['roadmap'] = report
                    st.session_state['master_data']['role'] = role
                    st.success("Roadmap Ready!")
                    st.subheader(f"Analysis for {role}")
                    st.write(report['gap_analysis'])

# --- FEATURE 4: NETWORKING RECOMMENDATIONS ---
elif app_mode == "Networking Recommendations":
    st.markdown("<h1 class='main-title'>🌐 LinkedIn Networking Advisor</h1>", unsafe_allow_html=True)
    user_input = st.text_area("Paste a job description or bio:", height=200)
    
    if st.button("Generate Recommendations"):
        if user_input:
            with st.spinner("Searching leaders..."):
                advisor = NetworkAdvisor()
                results = advisor.get_recommendations(user_input)
                if "error" in results:
                    st.error(results["error"])
                else:
                    # Save to Session State for Master Report
                    st.session_state['master_data']['networking'] = results
                    st.success("Leaders Found!")
                    for person in results.get("recommendations", []):
                        st.write(person)

# --- MASTER REPORT SIDEBAR LOGIC ---
st.sidebar.markdown("---")
st.sidebar.subheader("🎓 Master Career Bundle")
# Calculate completion progress
completed = sum(1 for k in ['profile', 'roadmap', 'networking'] if st.session_state['master_data'][k])
st.sidebar.progress(completed / 3)

if completed == 3:
    if st.sidebar.button("📦 Build Master Report"):
        pdf_tool = PDFReport()
        master_pdf = pdf_tool.generate_master_report(st.session_state['master_data'])
        st.sidebar.download_button("📥 Download Full Bundle", master_pdf, "Full_Career_Audit.pdf")
elif completed > 0:
    st.sidebar.info(f"Complete {3-completed} more sections to unlock the Master Report.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='text-align: center; color: #888;'>Created by <b>Abdel Kader Ahmed</b></div>", unsafe_allow_html=True)