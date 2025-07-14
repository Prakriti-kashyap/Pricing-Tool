# 1. --- MUST BE FIRST ---
import streamlit as st
st.set_page_config(layout="wide", page_title="Pricing Tool")

# 2. --- THEN OTHER IMPORTS ---
import os
import base64
from db import get_options_by_category
from utils import load_icon
from config import display_names, icon_paths

# 3. --- THEN LOAD ICONS, CSS, ETC. ---


# --- Load all icons from paths ---
icon_section_app_seg = load_icon(icon_paths["section_app_seg"])
icon_section_mmw     = load_icon(icon_paths["section_mmw"])
icon_section_packing = load_icon(icon_paths["section_packing"])
icon_tool_title      = load_icon(icon_paths["tool_title"])
icon_selection_sum   = load_icon(icon_paths["selection_sum"])
icon_grand_total     = load_icon(icon_paths["grand_total"])
icon_calc_total_btn  = load_icon(icon_paths["calc_total_btn"])
icon_logo_missing    = load_icon(icon_paths["logo_missing"])
icon_welcome         = load_icon(icon_paths["welcome"])
icon_features        = load_icon(icon_paths["features"])



# --- LOAD CUSTOM CSS ---
def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("styles.css")

# --- Load categories from DB ---
categories = [
    "Applications", "Segment", "Machine",
    "MeshMicro", "Whiteness", "Packing_Kg", "Packing_Type"
]


# --- Load pricing data from DB ---
catalog = {
    category: get_options_by_category(category)
    for category in categories
}

# --- LOGO LOADER ---
logo_path = "D:/Pricing tool/icons/Golcha-Logo.png"
if os.path.exists(logo_path):
    encoded_logo = base64.b64encode(open(logo_path, "rb").read()).decode()

    def render_logo(header_text):
        return f"""
        <div class="golcha-logo-wrapper">
            <h1 class="pricing-title">{header_text}</h1>
            <img src="data:image/png;base64,{encoded_logo}" alt="Golcha Logo" class="golcha-logo">
        </div>
        """
else:
    # use fallback icon
    fallback_icon = load_icon(icon_paths["logo_missing"])
    def render_logo(header_text):
        return f"""
        <div class="golcha-logo-wrapper">
            <h1 class="pricing-title">
                <img src="data:image/png;base64,{fallback_icon}" style="height: 30px; vertical-align: middle; margin-right: 10px;" />
                {header_text}
            </h1>
        </div>
        """


# --- SIDEBAR NAVIGATION ---
page = st.sidebar.radio("🔘 Navigate", [" Home", " Price Calculator"])

# --- HOME PAGE ---
if page == " Home":
    st.markdown(render_logo(f'<img src="data:image/png;base64,{icon_welcome}" height="32" style="vertical-align: left; margin-right: 10px;"> Welcome to the Pricing Tool'), unsafe_allow_html=True)

    st.markdown(f"""
        ### <img src="data:image/png;base64,{icon_features}" height="30" style="vertical-align: middle; margin-right: 8px;"> Features:
        - Organized dropdowns with quantity input  
        - Dynamic total calculation  
        - Custom styling and branding  
    """, unsafe_allow_html=True)


# --- PRICE CALCULATOR PAGE ---
elif page == " Price Calculator":
    st.markdown(f"""
        <div class="logo-title-bar" style="display: flex; align-items: center; gap: 20px; margin-top: 10px;">
            <img src="data:image/png;base64,{icon_tool_title}" style="height: 48px;" />
            <h1 style="font-size: 40px; font-weight: 800; margin: 0;">Pricing Tool</h1>
        </div>
    """, unsafe_allow_html=True)


    st.markdown('<div class="after-title-gap"></div>', unsafe_allow_html=True)

    # --- Reset Function ---
    def reset_all():
        for key in list(st.session_state.keys()):
            if key.endswith("_select"):
                st.session_state[key] = "-- Select --"
        st.experimental_rerun()

    if st.button("🧹 Reset Selections"):
        reset_all()

    selected_items = {}

    # --- Dropdown Renderer ---
    def render_dropdown_section(category, key_prefix=""):
        options_dict = catalog.get(category, {})
        if not options_dict:
            st.warning(f"No options found for: {category}")
            return

        display_label = display_names.get(category, category)

        # Load icon for this dropdown
        icon_base64 = ""
        icon_path = icon_paths.get(category)
        if icon_path:
            icon_base64 = load_icon(icon_path)

        st.markdown(f"""
            <div class="icon-title">
                <img src="data:image/png;base64,{icon_base64}" style="height: 24px; margin-right: 8px;" />
                <span>{display_label}</span>
            </div>
        """, unsafe_allow_html=True)

        choice = st.selectbox(
            label="",
            options=["-- Select --"] + list(options_dict.keys()),
            key=f"{key_prefix}_select"
        )
        if choice != "-- Select --":
            selected_items[f"{display_label} > {choice}"] = (category, choice)


    # --- Applications & Segment ---
    st.markdown(f"""
        <div class="section-heading">
            <img src="data:image/png;base64,{icon_section_app_seg}" style="height: 32px; vertical-align: middle; margin-right: 10px;" />
            Applications & Segment
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        render_dropdown_section("Applications", key_prefix="app")

    with col2:
        render_dropdown_section("Segment", key_prefix="seg")

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Machine, Mesh, Whiteness ---
    st.markdown(f"""
        <div class="section-heading">
            <img src="data:image/png;base64,{icon_section_mmw}" style="height: 32px; vertical-align: middle; margin-right: 10px;" />
            Machine, Mesh & Whiteness
        </div>
    """, unsafe_allow_html=True)


    col3, col4, col5 = st.columns(3, gap="large")
    with col3:
        render_dropdown_section("Machine", key_prefix="mach")

    with col4:
        render_dropdown_section("MeshMicro", key_prefix="mesh" )
    with col5:
        render_dropdown_section("Whiteness", key_prefix="white")

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Packing ---
    st.markdown(f"""
        <div class="section-heading">
            <img src="data:image/png;base64,{icon_section_packing}" style="height: 30px; vertical-align: middle; margin-right: 10px;" />
            Packing
        </div>
    """, unsafe_allow_html=True)

    col6, col7 = st.columns(2, gap="large")
    with col6:
        render_dropdown_section("Packing_Kg", key_prefix="Kg")
    with col7:
        render_dropdown_section("Packing_Type", key_prefix="ptype")

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Calculate Button ---
    if st.button(" Calculate Total"):
        if selected_items:
            total = 0
            st.markdown(f"""
                <h3 style="display: flex; align-items: center;">
                    <img src="data:image/png;base64,{icon_selection_sum}" height="30" style="margin-right: 10px;" />
                    Selection Summary
                </h3>
            """, unsafe_allow_html=True)

            for display_name, (category, item) in selected_items.items():
                price = catalog[category].get(item, 0)
                st.markdown(f"- **{display_name}**")
                total += price
            st.markdown(f"""
                <div style="display: flex; align-items: center; background-color: #d4edda; color: #155724;
                            padding: 12px 20px; border-radius: 8px; border-left: 6px solid #28a745;
                            font-size: 20px; margin-top: 20px;">
                    <img src="data:image/png;base64,{icon_grand_total}" height="30" style="margin-right: 12px;" />
                    <strong>Grand Total: ₹{total}</strong>
                </div>
            """, unsafe_allow_html=True)
            


        else:
            st.warning(" Please select at least one option.")

