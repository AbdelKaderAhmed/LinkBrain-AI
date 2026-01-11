import streamlit as st
from brain.profile_analyzer import ProfileAnalyzer # Import your logic

st.set_page_config(page_title="LinkBrain AI", layout="wide")

st.title("🧠 LinkBrain AI")

# Sidebar
st.sidebar.header("Control Panel")
option = st.sidebar.selectbox("Select Tool", ["Profile Optimizer"])

if option == "Profile Optimizer":
    st.subheader("🔍 Profile Optimization Engine")
    user_input = st.text_area("Paste your LinkedIn About/Experience here:", height=200)

    if st.button("Start Analysis"):
        if user_input:
            with st.spinner("Analyzing... please wait."):
                # 1. Initialize the analyzer
                analyzer = ProfileAnalyzer()
                # 2. Get the result
                result = analyzer.analyze_profile(user_input)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    # 3. Display Results in UI
                    st.metric("Profile Score", f"{result['score']}/100")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success("### Strengths")
                        for s in result['strengths']: st.write(f"- {s}")
                    with col2:
                        st.warning("### Weaknesses")
                        for w in result['weaknesses']: st.write(f"- {w}")
                    
                    st.info(f"**Summary:** {result['summary']}")
        else:
            st.error("Input cannot be empty!")