
import streamlit as st
from catalog import catalog

def show_variety_selection():
    st.subheader("🔘 Step 2: Select Varieties")

    selected_varieties = {}
    for cat in st.session_state.categories:
        with st.expander(f"🍱 {cat} Varieties"):
            varieties = st.multiselect(
                f"Select {cat} Varieties",
                list(catalog[cat].keys()),
                key=f"{cat}_varieties"
            )
            selected_varieties[cat] = varieties

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            st.session_state.varieties = selected_varieties
            st.session_state.step = 3
            st.rerun()
