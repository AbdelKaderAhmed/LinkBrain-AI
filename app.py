import streamlit as st
from dotenv import load_dotenv
import os

# Import custom modules from the brain folder
from brain.profile_analyzer import ProfileAnalyzer
from brain.post_generator import PostGenerator

# Load environment variables (API Keys)
load_dotenv()

# 1. Page Configuration
st.set_page_config(
    page_title="LinkBrain AI | Professional LinkedIn Assistant",
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
app_mode = st.sidebar.selectbox("Select a Tool:", ["Profile Optimizer", "Post Generator", "Skill Advisor"])

# --- FEATURE 1: PROFILE OPTIMIZER ---
if app_mode == "Profile Optimizer":
    st.markdown("<h1 class='main-title'>🔍 LinkedIn Profile Optimizer</h1>", unsafe_allow_html=True)
    st.write("Analyze your 'About' or 'Experience' section to improve recruiter visibility.")
    
    profile_input = st.text_area("Paste your profile text here:", height=250, placeholder="Example: Software Engineer with 5 years of experience...")
    
    if st.button("Analyze My Impact"):
        if profile_input:
            with st.spinner("LinkBrain is auditing your profile..."):
                try:
                    # Initialize the analyzer engine
                    analyzer = ProfileAnalyzer()
                    result = analyzer.analyze_profile(profile_input)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success("Analysis Complete!")
                        
                        # Score and Summary Display
                        col_score, col_sum = st.columns([1, 3])
                        with col_score:
                            st.metric("Profile Score", f"{result['score']}/100")
                        with col_sum:
                            st.subheader("Summary")
                            st.write(result['summary'])
                        
                        st.markdown("---")
                        
                        # Detailed Analysis
                        col_left, col_right = st.columns(2)
                        with col_left:
                            st.subheader("✅ Strengths")
                            for s in result['strengths']: st.write(f"- {s}")
                        with col_right:
                            st.subheader("⚠️ Weaknesses")
                            for w in result['weaknesses']: st.write(f"- {w}")
                        
                        st.markdown("---")
                        st.subheader("💡 Actionable Tips")
                        for tip in result['actionable_tips']:
                            st.info(tip)
                except Exception as e:
                    st.error(f"Error connecting to AI: {e}")
        else:
            st.warning("Please enter some text to analyze.")

# --- FEATURE 2: POST GENERATOR ---
elif app_mode == "Post Generator":
    st.markdown("<h1 class='main-title'>✍️ AI Content Creator</h1>", unsafe_allow_html=True)
    st.write("Generate high-engagement LinkedIn posts in seconds.")
    
    # Input Layout
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        topic = st.text_input("What is the post about?", placeholder="e.g., Lessons learned from my coding bootcamp")
        language = st.selectbox("Output Language:", ["English", "Arabic", "French"])
    with col_input2:
        tone = st.selectbox("Tone of Voice:", ["Professional", "Storytelling", "Educational", "Inspirational"])
    
    if st.button("Generate Post ✨"):
        if topic:
            with st.spinner("Drafting your post..."):
                try:
                    # Initialize the generator engine
                    gen = PostGenerator()
                    post_content = gen.generate_post(topic, tone, language)
                    
                    st.markdown("---")
                    st.subheader("Generated Content:")
                    
                    # Apply RTL class if Arabic is selected
                    dir_class = "rtl-text" if language == "Arabic" else ""
                    st.markdown(f'<div class="{dir_class}">{post_content}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Generation failed: {e}")
        else:
            st.warning("Please provide a topic first.")

# --- FEATURE 3: SKILL ADVISOR (Placeholder) ---
elif app_mode == "Skill Advisor":
    st.header("📊 Market Skill Advisor")
    st.info("This feature is under development. It will soon help you identify skill gaps in your industry.")
# Custom Footer with your name
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='text-align: center; color: #888888;'>"
    "Created by <b> Abdel Kader Ahmed</b>"
    "</div>", 
    unsafe_allow_html=True
)