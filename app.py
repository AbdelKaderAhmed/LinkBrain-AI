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

# Load environment variables (API Keys)
load_dotenv()

# 1. Page Configuration
st.set_page_config(
    page_title="LinkBrain AI | Career Intelligent Hub",
    page_icon="🧠",
    layout="wide"
)

# 2. Global Professional Styling (CSS)
st.markdown("""
    <style>
    /* Support for Right-to-Left (RTL) text for Arabic */
    .rtl-text {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #0A66C2; /* LinkedIn Brand Blue */
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #0A66C2;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation
st.sidebar.markdown("<h2 style='text-align: center;'>🧠 LinkBrain Menu</h2>", unsafe_allow_html=True)

# Corrected selectbox to include the fourth option
app_mode = st.sidebar.selectbox("Select a Tool:", 
    ["Profile Optimizer", "Post Generator", "Skill Advisor", "Networking Recommendations"]
)

# --- FEATURE 1: PROFILE OPTIMIZER ---
if app_mode == "Profile Optimizer":
    st.markdown("<h1 class='main-title'>🔍 LinkedIn Profile Optimizer</h1>", unsafe_allow_html=True)
    st.write("Refine your profile content for maximum professional impact.")
    
    profile_input = st.text_area("Paste your profile text here:", height=250)
    
    if st.button("Analyze My Profile"):
        if profile_input:
            with st.spinner("Analyzing..."):
                analyzer = ProfileAnalyzer()
                result = analyzer.analyze_profile(profile_input)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Analysis Complete!")
                    col_score, col_sum = st.columns([1, 3])
                    with col_score:
                        st.metric("Profile Score", f"{result['score']}/100")
                    with col_sum:
                        st.subheader("Summary")
                        st.write(result['summary'])
                    
                    st.markdown("---")
                    col_left, col_right = st.columns(2)
                    with col_left:
                        st.subheader("✅ Strengths")
                        for s in result['strengths']: st.write(f"- {s}")
                    with col_right:
                        st.subheader("⚠️ Weaknesses")
                        for w in result['weaknesses']: st.write(f"- {w}")
        else:
            st.warning("Please provide profile text.")

# --- FEATURE 2: POST GENERATOR ---
elif app_mode == "Post Generator":
    st.markdown("<h1 class='main-title'>✍️ AI Content Creator</h1>", unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        topic = st.text_input("Post Topic:", placeholder="e.g., Remote work benefits")
        language = st.selectbox("Language:", ["English", "Arabic", "French"])
    with col_input2:
        tone = st.selectbox("Tone:", ["Professional", "Storytelling", "Educational"])
    
    if st.button("Generate Post ✨"):
        if topic:
            with st.spinner("Writing..."):
                gen = PostGenerator()
                post_content = gen.generate_post(topic, tone, language)
                st.markdown("---")
                dir_class = "rtl-text" if language == "Arabic" else ""
                st.markdown(f'<div class="{dir_class}">{post_content}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter a topic.")

# --- FEATURE 3: SKILL ADVISOR ---
elif app_mode == "Skill Advisor":
    st.markdown("<h1 class='main-title'>📊 Market Skill Advisor</h1>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        role = st.text_input("Target Job Role:", placeholder="e.g., Frontend Developer")
    with col_b:
        lang = st.selectbox("Language:", ["English", "Arabic", "French"])
        
    skills_input = st.text_area("Your Current Skills:", placeholder="HTML, CSS, JavaScript...")

    if st.button("Get Career Roadmap 🚀"):
        if role and skills_input:
            with st.spinner("Generating roadmap..."):
                advisor = SkillAdvisor()
                report = advisor.analyze_skills(skills_input, role, lang)
                
                if "error" in report:
                    st.error(report["error"])
                else:
                    st.success("Roadmap Ready!")
                    dir_class = "rtl-text" if lang == "Arabic" else ""
                    st.markdown(f'<div class="{dir_class}">', unsafe_allow_html=True)
                    st.subheader(f"Analysis for {role}")
                    st.info(report['gap_analysis'])
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🛠 Technical")
                        for ts in report['tech_skills']: st.write(f"- {ts}")
                    with c2:
                        st.subheader("🤝 Soft Skills")
                        for ss in report['soft_skills']: st.write(f"- {ss}")
                    
                    st.markdown("---")
                    st.subheader("📅 3-Month Plan")
                    st.write(report['roadmap'])
                    st.markdown('</div>', unsafe_allow_html=True)

                    if lang != "Arabic":
                        try:
                            pdf_tool = PDFReport()
                            pdf_bytes = pdf_tool.generate_career_pdf(role, report)
                            st.download_button(
                                label="📥 Download Roadmap (PDF)",
                                data=pdf_bytes,
                                file_name=f"{role}_roadmap.pdf",
                                mime="application/pdf"
                            )
                        except Exception as e:
                            st.error(f"PDF Generation failed: {e}")
                    else:
                        st.warning("PDF export is available for English and French only.")
        else:
            st.warning("Fill in all fields.")

# --- FEATURE 4: NETWORKING RECOMMENDATIONS (Corrected Logic) ---
elif app_mode == "Networking Recommendations":
    st.markdown("<h1 class='main-title'>🌐 LinkedIn Networking Advisor</h1>", unsafe_allow_html=True)
    st.info("Find industry leaders to expand your professional network.")
    
    user_input = st.text_area("Paste a job description or your bio to find the right people:", height=200)
    
    if st.button("Generate Recommendations"):
        if user_input:
            with st.spinner("Searching for industry experts..."):
                advisor = NetworkAdvisor()
                results = advisor.get_recommendations(user_input)
                
                if "error" in results:
                    st.error(results["error"])
                else:
                    st.success(f"Top leaders in {results.get('target_niche', 'your field')}")
                    
                    for person in results.get("recommendations", []):
                        if "|" in person:
                            name, link, reason = person.split("|")
                            with st.container():
                                st.markdown(f"### 👤 {name.strip()}")
                                st.write(f"💡 **Why follow:** {reason.strip()}")
                                st.markdown(f"[🔗 View LinkedIn Profile]({link.strip()})")
                                st.divider()
        else:
            st.warning("Please provide some text to analyze.")

# --- CUSTOM FOOTER ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='text-align: center; color: #888888;'>"
    "Created by <b>Abdel Kader Ahmed </b>"
    "</div>", 
    unsafe_allow_html=True
)