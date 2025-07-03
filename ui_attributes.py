# --- 📁 file: ui_attributes.py ---
import streamlit as st
from catalog import catalog

def show_attribute_selection():
    st.subheader("⚪ Step 3: Choose Attributes & Quantity")

    selected_attrs = {}

    for category, var_list in st.session_state.varieties.items():
        for variety in var_list:
            with st.expander(f"🔧 {category} → {variety} Options"):
                for attr, price in catalog[category][variety].items():
                    attr_key = f"{category}_{variety}_{attr}"
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        checked = st.checkbox(f"{attr} — ₹{price}", key=f"{attr_key}_check")
                    if checked:
                        with col2:
                            qty = st.number_input(
                                "Qty", min_value=1, value=1, step=1, key=f"{attr_key}_qty"
                            )
                        selected_attrs[f"{category} > {variety} > {attr}"] = (price, qty)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Show Total 💰"):
            st.session_state.selected_attrs = selected_attrs
            st.session_state.step = 4
            st.rerun()
