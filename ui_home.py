
import streamlit as st
from catalog import catalog

def show_home():
    st.markdown("""
        <div class='title-style'>🧮 Multi-Step Price Configuration Tool</div>
    """, unsafe_allow_html=True)

    st.subheader("🔵 Step 1: Select Categories")
    st.markdown("Pick one or more categories to continue:")

    categories = st.multiselect("🧺 Choose Item Categories", list(catalog.keys()))

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next ➡️"):
            if categories:
                st.session_state.categories = categories
                st.session_state.step = 2
                st.rerun()
            else:
                st.warning("Please select at least one category.")