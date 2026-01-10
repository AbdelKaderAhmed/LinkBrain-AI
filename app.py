import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables (API Keys)
load_dotenv()

# Page configuration
st.set_page_config(page_title="LinkBrain AI", page_icon="🧠", layout="wide")

st.title("🧠 LinkBrain AI")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a tool:", ["Profile Optimizer", "Post Generator", "Skill Advisor"])

if app_mode == "Profile Optimizer":
    st.header("🔍 LinkedIn Profile Optimizer")
    profile_input = st.text_area("Paste your LinkedIn 'About' or 'Experience' section here:", height=200)
    
    if st.button("Analyze Profile"):
        if profile_input:
            st.write("🔄 Analysis in progress... (Waiting for Brain module)")
        else:
            st.warning("Please paste some text first!")