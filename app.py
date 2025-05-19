import streamlit as st
import pandas as pd
import numpy as np
from utils.data_helpers import load_sample_scenarios

# Set page configuration
st.set_page_config(
    page_title="CyberRiskQuant - FAIR Risk Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Main page header
    st.title("CyberRiskQuant 🛡️")
    st.subheader("Cybersecurity Risk Quantification using FAIR Model")
    
    # Introduction to the tool
    st.markdown("""
    ## Welcome to CyberRiskQuant
    
    This tool helps you quantify cybersecurity risks in financial terms using the **Factor Analysis of Information Risk (FAIR)** model 
    and Monte Carlo simulations.
    
    ### What is FAIR?
    FAIR is a framework for understanding, analyzing, and measuring information risk. It provides a model for understanding the factors 
    that contribute to risk and how they affect each other.
    
    ### How to use this tool:
    1. Navigate to the **Risk Analysis** page to analyze your own risk scenarios
    2. Explore pre-built **Case Studies** to understand real-world applications
    3. Visit the **Educational Resources** page to learn more about GRC concepts
    
    ### Key Benefits:
    - Quantify cybersecurity risks in monetary terms
    - Make data-driven decisions about security investments
    - Communicate risk effectively to stakeholders
    - Prioritize security initiatives based on financial impact
    """)
    
    # Quick start section
    st.header("Quick Start")
    st.markdown("""
    Want to see how the tool works? Choose a sample scenario below to get started:
    """)
    
    # Load sample scenarios
    sample_scenarios = load_sample_scenarios()
    selected_scenario = st.selectbox("Select a sample scenario:", 
                                   list(sample_scenarios.keys()),
                                   key="scenario_selector")  # Added unique key
    
    if st.button("Analyze Sample Scenario", key="analyze_button"):  # Added unique key
        st.session_state["selected_sample"] = selected_scenario
        st.switch_page("pages/1_Risk_Analysis.py")
    
    # Footer with additional information
    st.markdown("---")
    st.markdown("""
    CyberRiskQuant is designed to help organizations better understand and quantify their cybersecurity risks.
    Use the navigation menu on the left to explore different sections of the application.
    """)

if __name__ == "__main__":
    main()
