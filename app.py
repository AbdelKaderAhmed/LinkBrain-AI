import streamlit as st
from dotenv import load_dotenv
import os

import time
from database import log_performance

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

with st.sidebar:
    st.divider()  # Visual separator for better organization
    
    if st.button("🔄 Reset Application", use_container_width=True):
        # Clear all data stored in the current session state
        for key in st.session_state.keys():
            del st.session_state[key]
        
        # Immediately restart the application to reflect changes
        st.rerun()

# 2. Initialize Session State for Master Report
# This keeps data alive when switching between sidebar menu options
if 'master_data' not in st.session_state:
    st.session_state['master_data'] = {
        'profile': None,
        'roadmap': None,
        'networking': None,
        'role': ""
    }

st.set_page_config(page_title="LinkBrain AI", page_icon="🧠", layout="wide")

# Custom CSS for Professional Branding
st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp {
        background-color: black; /* LinkedIn light gray background */
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: black;
        border-right: 1px solid #e0e0e0;
    }

    /* Professional Titles */
    .main-title {
        color: #0a66c2;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        text-align: center;
        padding: 20px;
    }

    /* Card-style containers for features */
    .stCard {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }

    /* Buttons Styling */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        border: 1px solid #0a66c2;
        background-color: white;
        color: #0a66c2;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0a66c2;
        color: white;
    }
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
        start_time = time.time()
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
        end_time = time.time() # 
        latency = round(end_time - start_time, 2)
        


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
            start_time = time.time()

            with st.spinner("Writing..."):
                try:
                    gen = PostGenerator()
                    post_content = gen.generate_post(topic, tone, language)
                    
                    # 2. 
                    latency = round(time.time() - start_time, 2)
                    
                    # 3. 
                    log_performance("Post Generator", latency, "Success", len(topic))
                    
                    dir_class = "rtl-text" if language == "Arabic" else ""
                    st.markdown(f'<div class="{dir_class}">{post_content}</div>', unsafe_allow_html=True)
                    st.success(f"Generated in {latency}s") # اختياري: إظهار السرعة للمطور
                    
                except Exception as e:
                    # 4. تسجيل الفشل في حال حدوث خطأ
                    log_performance("Post Generator", 0, f"Error: {str(e)[:20]}", len(topic))
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please provide a topic.")

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
            start_time = time.time()
            
            with st.spinner("Generating your personalized roadmap..."):
                try:
                    # Initialize logic from brain folder
                    advisor = SkillAdvisor()
                    report = advisor.analyze_skills(skills_input, role, lang)
                    
                    # 2. حساب الوقت المستغرق
                    latency = round(time.time() - start_time, 2)
                    
                    if "error" in report:
                        # 
                        log_performance("Skill Advisor", latency, "Error", len(skills_input))
                        st.error(report["error"])
                    else:
                        # 3. 
                        log_performance("Skill Advisor", latency, "Success", len(skills_input))
                        
                        # Sync data to Session State for the Master PDF Report
                        st.session_state['master_data']['roadmap'] = report
                        st.session_state['master_data']['role'] = role
                        
                        st.success(f"Roadmap Ready! (Processed in {latency}s)")
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
                        
                except Exception as e:
                    # تسجيل أي انهيار مفاجئ في النظام
                    log_performance("Skill Advisor", 0, f"Crash: {str(e)[:20]}", len(skills_input))
                    st.error(f"System Error: {e}")
        else:
            st.warning("Please fill in both the Target Role and Current Skills.")

# --- FEATURE 4: NETWORKING RECOMMENDATIONS ---
elif app_mode == "Networking Recommendations":
    st.markdown("<h1 class='main-title'>🌐 LinkedIn Networking Advisor</h1>", unsafe_allow_html=True)
    user_input = st.text_area("Paste a job description or bio:", height=200)
    
    if st.button("Generate Recommendations"):
        if user_input:

            start_time = time.time()
            
            with st.spinner("Searching leaders..."):
                try:
                    advisor = NetworkAdvisor()
                    results = advisor.get_recommendations(user_input)
                    
                    # 2.
                    latency = round(time.time() - start_time, 2)
                    
                    if "error" in results:
                        # 
                        log_performance("Networking Advisor", latency, f"Error: {results['error'][:15]}", len(user_input))
                        st.error(results["error"])
                    else:
                        # 3.
                        log_performance("Networking Advisor", latency, "Success", len(user_input))
                        
                        # Save to Session State for Master Report
                        st.session_state['master_data']['networking'] = results
                        st.success(f"Leaders Found! (in {latency}s)")
                        
                        for person in results.get("recommendations", []):
                            st.write(person)
                            
                except Exception as e:
                    # 
                    log_performance("Networking Advisor", 0, f"Crash: {str(e)[:15]}", len(user_input))
                    st.error(f"System Error: {e}")
        else:
            st.warning("Please provide input text.")
# --- MASTER REPORT SIDEBAR LOGIC ---
st.sidebar.markdown("---")
st.sidebar.subheader("🎓 Master Career Bundle")
# Calculate completion progress
completed = sum(1 for k in ['profile', 'roadmap', 'networking'] if st.session_state['master_data'][k])
st.sidebar.progress(completed / 3)

if completed == 3:
    if st.sidebar.button("📦 Build Master Report"):
        start_time = time.time()
        
        with st.spinner("Generating PDF Bundle..."):
            try:
                pdf_tool = PDFReport()
                master_pdf = pdf_tool.generate_master_report(st.session_state['master_data'])
                
                # 2.
                latency = round(time.time() - start_time, 2)
                
                # 3. 
                log_performance("Master PDF Report", latency, "Success", 100) # 100 كقيمة افتراضية للحجم
                
                st.sidebar.download_button("📥 Download Full Bundle", master_pdf, "Full_Career_Audit.pdf")
                st.sidebar.success(f"Report Generated in {latency}s")
                
            except Exception as e:
                # تسجيل الفشل إذا حدث خطأ في مكتبة الـ PDF
                log_performance("Master PDF Report", 0, f"PDF Error: {str(e)[:15]}", 0)
                st.sidebar.error("Failed to build PDF.")

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
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        chat_box = st.container(height=350)

        for msg in st.session_state.messages:
            avatar = "👤" if msg["role"] == "user" else "🧠"
            with chat_box.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        if chat_input := st.chat_input("Type your message..."):
            # 1. ابدأ التوقيت عند إرسال المستخدم للرسالة
            import time
            from database import log_performance
            start_time = time.time()
            
            st.session_state.messages.append({"role": "user", "content": chat_input})
            with chat_box.chat_message("user", avatar="👤"):
                st.markdown(chat_input)

            with st.spinner("Analyzing..."):
                try:
                    context = st.session_state.get('master_data', {}).get('profile')
                    coach = CareerCoach()
                    response = coach.get_response(st.session_state.messages, context_data=context)
                    
                    # 2. حساب وقت الاستجابة
                    latency = round(time.time() - start_time, 2)
                    
                    # 3. تسجيل الأداء في لوحة المطور
                    log_performance("AI Coach Chat", latency, "Success", len(chat_input))
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    with chat_box.chat_message("assistant", avatar="🧠"):
                        st.markdown(response)
                        
                except Exception as e:
                    # تسجيل الفشل في حال انقطاع الـ API أثناء المحادثة
                    log_performance("AI Coach Chat", 0, f"Chat Error: {str(e)[:15]}", len(chat_input))
                    st.error("I'm having trouble thinking right now. Please try again.")

        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='text-align: center; color: #888;'>Created by <b>Abdel Kader Ahmed</b></div>", unsafe_allow_html=True)