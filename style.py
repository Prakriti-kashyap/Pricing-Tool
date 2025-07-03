# --- 📁 file: style.py ---
import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .title-style {
            font-size: 2.2em; 
            font-weight: bold;
            color: #34495e;
            text-align: center;
            margin-bottom: 1rem;
        }
        .section-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 1rem;
        }
        .card {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
