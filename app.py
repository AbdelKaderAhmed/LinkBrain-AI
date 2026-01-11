import streamlit as st
from brain.profile_analyzer import ProfileAnalyzer

# 1. Page Configuration
st.set_page_config(
    page_title="LinkBrain AI | LinkedIn Optimizer",
    page_icon="🧠",
    layout="wide"
)

# 2. Custom CSS for RTL support and Styling
st.markdown("""
    <style>
    /* Support for Arabic text direction */
    .rtl-text {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #0A66C2; /* LinkedIn Blue */
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown("<h1 class='main-title'>🧠 LinkBrain AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Optimize your LinkedIn presence in English, Arabic, or French.</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Sidebar Navigation
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Choose a tool:", ["Profile Optimizer", "Post Generator", "Skill Advisor"])

if app_mode == "Profile Optimizer":
    st.header("🔍 LinkedIn Profile Optimizer")
    
    # Input area
    profile_input = st.text_area(
        "Paste your 'About' or 'Experience' section here:",
        placeholder="Example: I am a Software Engineer...",
        height=250
    )
    
    if st.button("Analyze Impact"):
        if profile_input:
            with st.spinner("LinkBrain is analyzing your profile..."):
                try:
                    # Initialize the logic engine
                    analyzer = ProfileAnalyzer()
                    result = analyzer.analyze_profile(profile_input)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success("Analysis Complete!")
                        
                        # Displaying Metrics
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.metric("Profile Score", f"{result['score']}/100")
                        with col2:
                            st.subheader("Summary")
                            st.write(result['summary'])
                        
                        st.markdown("---")
                        
                        # Results columns
                        left_col, right_col = st.columns(2)
                        with left_col:
                            st.subheader("✅ Strengths")
                            for item in result['strengths']:
                                st.write(f"✔️ {item}")
                                
                        with right_col:
                            st.subheader("⚠️ Weaknesses")
                            for item in result['weaknesses']:
                                st.write(f"❌ {item}")
                        
                        st.markdown("---")
                        st.subheader("💡 Actionable Tips")
                        for tip in result['actionable_tips']:
                            st.info(tip)
                            
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        else:
            st.warning("Please paste some text before clicking analyze.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Powered by OpenAI & Streamlit")