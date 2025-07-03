# --- 📁 file: main.py ---
import streamlit as st
from ui_home import show_home
from ui_varieties import show_variety_selection
from ui_attributes import show_attribute_selection
from ui_summary import show_price_summary

# --- Session State Defaults ---
def initialize_state():
    defaults = {
        "step": 1,
        "categories": [],
        "varieties": {},
        "selected_attrs": {}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# --- Init ---
st.set_page_config(page_title="Price Tool", layout="centered")
initialize_state()

# --- Step Control ---
step = st.session_state.step
if step == 1:
    show_home()
elif step == 2:
    show_variety_selection()
elif step == 3:
    show_attribute_selection()
elif step == 4:
    show_price_summary()