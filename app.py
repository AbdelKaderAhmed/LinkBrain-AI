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

# Import the new CareerCoach class from the brain folder
from brain.career_coach import CareerCoach
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


# --- FEATURE 1: PROFILE OPTIMIZER (Updated View) ---
if app_mode == "Profile Optimizer":
    st.markdown("<h1 class='main-title'>🔍 LinkedIn Profile Optimizer</h1>", unsafe_allow_html=True)
    profile_input = st.text_area("Paste your profile text here:", height=250)
    
    if st.button("Analyze My Profile"):
        if profile_input:
            with st.spinner("Analyzing profile structure..."):
                analyzer = ProfileAnalyzer()
                result = analyzer.analyze_profile(profile_input)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    # Save to Session State for Master Report
                    st.session_state['master_data']['profile'] = result
                    
                    st.success("Analysis Complete!")
                    
                    # --- Display Score & Summary ---
                    col_score, col_sum = st.columns([1, 2])
                    with col_score:
                        st.metric("Profile Score", f"{result.get('score', 0)}/100")
                    with col_sum:
                        st.subheader("📝 Professional Summary")
                        st.write(result.get('summary', 'No summary generated.'))
                    
                    st.divider()

                    # --- Display SWOT (Strengths & Weaknesses) ---
                    st.subheader("⚖️ SWOT Analysis")
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.markdown("#### ✅ Strengths")
                        strengths = result.get('strengths', [])
                        for s in strengths:
                            st.success(s) # Uses green boxes for strengths
                            
                    with col_right:
                        st.markdown("#### ⚠️ Areas for Improvement")
                        weaknesses = result.get('weaknesses', [])
                        for w in weaknesses:
                            st.warning(w) # Uses yellow/orange boxes for weaknesses
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
    
    # Input Layout
    col_a, col_b = st.columns(2)
    with col_a:
        role = st.text_input("Target Job Role:", placeholder="e.g., Full Stack Developer")
    with col_b:
        lang = st.selectbox("Language:", ["English", "Arabic", "French"])
        
    skills_input = st.text_area("Your Current Skills:", placeholder="e.g., Python, React, SQL")

    if st.button("Get Career Roadmap 🚀"):
        if role and skills_input:
            with st.spinner("Generating your personalized roadmap..."):
                # Initialize logic from brain folder
                advisor = SkillAdvisor()
                report = advisor.analyze_skills(skills_input, role, lang)
                
                if "error" in report:
                    st.error(report["error"])
                else:
                    # Sync data to Session State for the Master PDF Report
                    st.session_state['master_data']['roadmap'] = report
                    st.session_state['master_data']['role'] = role
                    
                    st.success("Roadmap Ready!")
                    st.subheader(f"Analysis for {role}")
                    
                    # Display the initial Gap Analysis
                    st.info(report.get('gap_analysis', 'No gap analysis available.'))
                    
                    # Display Skill Categories in columns
                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🛠 Technical Skills")
                        for ts in report.get('tech_skills', []): 
                            st.write(f"- {ts}")
                    with c2:
                        st.subheader("🤝 Soft Skills")
                        for ss in report.get('soft_skills', []): 
                            st.write(f"- {ss}")
                    
                    st.divider()
                    
                    # Display the detailed 3-Month Roadmap
                    st.subheader("📅 3-Month Learning Plan")
                    st.markdown(report.get('roadmap', 'No detailed roadmap generated.'))
        else:
            st.warning("Please fill in both the Target Role and Current Skills.")

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

# --- PROFESSIONAL FLOATING-STYLE CHATBOT ---

# 1. Custom CSS to fix the chat to the bottom and style it like a professional widget
st.markdown("""
    <style>
    /* Main Chat Container */
    .stChatFloating {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        z-index: 1000;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border: 1px solid #e0e0e0;
    }
    /* Header Styling */
    .chat-header {
        background: #0a66c2;
        color: white;
        padding: 12px;
        border-radius: 15px 15px 0 0;
        font-weight: bold;
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Using an Expander at the bottom of the main page to simulate a "Pop-up"
# We place it inside a column to push it to the right
col1, col2 = st.columns([2, 1])

with col2:
    with st.expander("🧠 LinkBrain Assistant", expanded=False):
        st.markdown("<div class='chat-header'>🧠 Executive AI Coach</div>", unsafe_allow_html=True)
        
        # Initialize session state for messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Chat display area with fixed height
        chat_box = st.container(height=350)

        # Show message history
        for msg in st.session_state.messages:
            avatar = "👤" if msg["role"] == "user" else "🧠"
            with chat_box.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        # Chat Input
        if chat_input := st.chat_input("Type your message..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": chat_input})
            with chat_box.chat_message("user", avatar="👤"):
                st.markdown(chat_input)

            # AI Response Logic
            with st.spinner("Analyzing..."):
                context = st.session_state.get('master_data', {}).get('profile')
                coach = CareerCoach()
                response = coach.get_response(st.session_state.messages, context_data=context)
            
            # Add AI message
            st.session_state.messages.append({"role": "assistant", "content": response})
            with chat_box.chat_message("assistant", avatar="🧠"):
                st.markdown(response)
        
        # Reset Button inside the chat for convenience
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='text-align: center; color: #888;'>Created by <b>Abdel Kader Ahmed</b></div>", unsafe_allow_html=True)