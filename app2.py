# 1. --- MUST BE FIRST ---
import streamlit as st
import os
import base64
from db import get_options_by_category, authenticate_user, get_connection
from config import display_names, icon_paths
from decimal import Decimal, InvalidOperation
from utils import load_icon

st.set_page_config(layout="wide", page_title="Pricing Tool")

# --- ICON HELPERS ---
def encode_icon(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    else:
        st.warning(f"Icon not found: {path}")
        return ""

def load_icon_html(icon_base64, width=24, height=None):
    size_attr = f'width="{width}"' if height is None else f'width="{width}" height="{height}"'
    return f'<img src="data:image/png;base64,{icon_base64}"' \
           f' {size_attr} style="vertical-align: middle; margin-right: 8px;">'


# 2. --- DB & CATALOG LOAD ---
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT DB_NAME()")
current_db = cursor.fetchone()[0]
cursor.execute("SELECT name FROM sys.tables")
tables = [row[0] for row in cursor.fetchall()]
cursor.close()
conn.close()


# 3. --- ICONS LOAD ---
icon_section_app_seg = encode_icon(icon_paths["section_app_seg"])
icon_section_mmw = encode_icon(icon_paths["section_mmw"])
icon_section_packing = encode_icon(icon_paths["section_packing"])
icon_tool_title = encode_icon(icon_paths["tool_title"])
icon_selection_sum = encode_icon(icon_paths["selection_sum"])
icon_grand_total = encode_icon(icon_paths["grand_total"])
icon_logo_missing = encode_icon(icon_paths["logo_missing"])
icon_welcome = encode_icon(icon_paths["welcome"])
icon_features = encode_icon(icon_paths["features"])
icon_signup = encode_icon(icon_paths["signup"])


# 4. --- CUSTOM CSS ---
def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("styles.css")

# 5. --- Load pricing catalog ---
categories = ["Applications", "Segment", "Location", "Machine", "Control", "Whiteness", "MeshMicro", "Packing_Kg", "Packing_Type"]
catalog = {category: get_options_by_category(category) for category in categories}

# 6. --- LOGO + HEADER FUNCTION ---
logo_path = "D:/Pricing tool/icons/Golcha-Logo.png"
encoded_logo = encode_icon(logo_path)

def render_logo_with_title(title_text="Pricing Tool", icon_base64=icon_tool_title):
    return f"""
    <div class="golcha-header-row">
        <div class="title-icon-block" style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{icon_base64}" style="height: 90px; margin-right: 12px;" />
            <h1 class="pricing-title">{title_text}</h1> 
        </div>
        <div class="golcha-logo-wrapper">
            <img src="data:image/png;base64,{encoded_logo}" 
            alt="Golcha Logo" class="golcha-logo" style="height: 120px;">
        </div>
    </div>
    """

# 7. --- SESSION LOGIN ---


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

if not st.session_state["logged_in"]:
    st.markdown(render_logo_with_title("Welcome to the Golcha Pricing Tool", icon_welcome), unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background-color: #eef5f9; padding: 20px; border-radius: 12px; margin-bottom: 30px;">
            <h4 style="margin-top: 0;">
                {load_icon_html(icon_features, height=24)}
                Features at a Glance
            </h4>
            <ul style="line-height: 1.6;">
                <li>🎯 Organized dropdown selections by category</li>
                <li>🧮 Dynamic price calculation & summary</li>
                <li>🖍️ Fully customized UI & branding</li>
                <li>🔐 Secure login with password hashing</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div style="background-color: #fff; padding: 30px; border-radius: 16px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.08);">
                <h3 style="text-align: center;">
                    {load_icon_html(icon_signup, height=250 , width = 200)}
                    Log In to Continue
                </h3>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter username").strip().lower()
        password = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("🔐 Login"):
            if authenticate_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Login successful. Loading tool...")
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("#### New here? Create an account below:")

        with st.form("signup_form", clear_on_submit=True):
            new_username = st.text_input("👤 New Username", placeholder="Create a username").strip().lower()
            new_password = st.text_input("🔒 New Password", type="password", placeholder="Enter new password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password")
            submitted = st.form_submit_button("📝 Sign Up")

            if submitted:
                if not new_username or not new_password:
                    st.warning("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 8 or not any(char.isdigit() for char in new_password):
                    st.warning("Password must be at least 8 characters and include a number.")
                else:
                    from db import create_user
                    if create_user(new_username, new_password):
                        st.success("Account created successfully! Please log in above.")
                    else:
                        st.error("Username already exists. Try a different one.")

    st.stop()

st.markdown(render_logo_with_title("Pricing Tool", icon_tool_title), unsafe_allow_html=True)


# 7. --- RESET BUTTON ---
def reset_all():
    for key in list(st.session_state.keys()):
        if key.endswith("_select"):
            st.session_state[key] = "-- Select --"
    st.rerun()


col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("🔄 Reset"):
        reset_all()

with col3:
    if st.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()


# 8. --- DROPDOWN SECTION FUNCTION ---
def render_dropdown_section(category, key_prefix=""):
    options_dict = catalog.get(category, {})
    if not options_dict:
        st.warning(f"No options found for: {category}")
        return

    display_label = display_names.get(category, category)
    icon_base64 = ""
    icon_path = icon_paths.get(category)
    if icon_path:
        icon_base64 = load_icon(icon_path)

    st.markdown(f"""
        <div class="icon-title">
            <img src="data:image/png;base64,{icon_base64}"  />
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


selected_items = {}

# 9. --- SECTION: Applications & Segment ---
st.markdown(f"""
    <div class="section-heading">
        <img src="data:image/png;base64,{icon_section_app_seg}" 
        style="height: 50px; vertical-align: middle; margin-right: 10px;" />
        Applications , Segment  & Location
    </div>
""", unsafe_allow_html=True)

col1, col2 , col3 = st.columns(3, gap="large")
with col1:
    render_dropdown_section("Applications", key_prefix="app")
with col2:
    render_dropdown_section("Segment", key_prefix="seg")
with col3:
    render_dropdown_section("Locations", key_prefix="loc")

st.markdown("<hr>", unsafe_allow_html=True)

# 10. --- SECTION: Machine, Control, Whiteness ---
st.markdown(f"""
    <div class="section-heading">
        <img src="data:image/png;base64,{icon_section_mmw}" 
        style="height: 50px; vertical-align: middle; margin-right: 10px;" />
        Machine,Control & Whiteness
    </div>
""", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3, gap="large")
with col4:
    render_dropdown_section("Machine", key_prefix="mach")
with col5:
    render_dropdown_section("Control", key_prefix="con")
with col6:
    render_dropdown_section("Whiteness", key_prefix="white")

st.markdown("<hr>", unsafe_allow_html=True)

# 11. --- SECTION: Size & Packing ---
st.markdown(f"""
    <div class="section-heading">
        <img src="data:image/png;base64,{icon_section_packing}" 
        style="height: 50px; vertical-align: middle; margin-right: 10px;" />
        Size & Packing
    </div>
""", unsafe_allow_html=True)

col7, col8 , col9= st.columns(3, gap="large")
with col7:
    render_dropdown_section("MeshMicro", key_prefix="mesh")
with col8:
    render_dropdown_section("Packing_Kg", key_prefix="kg")
with col9:
    render_dropdown_section("Packing_Type", key_prefix="ptype")

st.markdown("<hr>", unsafe_allow_html=True)

# 12. --- CALCULATE TOTAL ---


if st.button(" Calculate Total"):
    selected_items = {}
    total = Decimal("0.00")

    # Map key_prefix to full category name
    prefix_to_category = {
        "app": "Applications",
        "seg": "Segment",
        "loc": "Location",
        "mach": "Machine",
        "mesh": "MeshMicro",
        "white": "Whiteness",
        "kg": "Packing_Kg",
        "ptype": "Packing_Type"
    }

    for prefix, category in prefix_to_category.items():
        select_key = f"{prefix}_select"
        selected_value = st.session_state.get(select_key, "-- Select --")

        if selected_value and selected_value != "-- Select --":
            display_name = display_names.get(category, category)
            selected_items[f"{display_name} > {selected_value}"] = (category, selected_value)

    # Display warning if no valid selections
    if not selected_items:
        st.warning("Please select at least one option.")
    else:
        # Section heading
        st.markdown(f"""
            <h3 style="display: flex; align-items: center ; background-color: #d4edda; color: #155724;
                        padding: 12px 20px; border-radius: 8px; border-left: 6px solid #28a745;
                        font-size: 20px; margin-top: 20px;;">
                <img src="data:image/png;base64,{icon_selection_sum}" height="50" style="margin-right: 12px;" />
                Selection Summary
            </h3>
        """, unsafe_allow_html=True)

        # Show each selection and accumulate total
        for display_name, (category, item) in selected_items.items():
            raw_price = catalog[category].get(item, "0")
            try:
                price = Decimal(str(raw_price))
            except InvalidOperation:
                price = Decimal("0.00")

            total += price
            st.markdown(f"- **{display_name}**")

        # Grand total display
        st.markdown(f"""
            <div style="display: flex; align-items: center; background-color: #d4edda; color: #155724;
                        padding: 12px 20px; border-radius: 8px; border-left: 6px solid #28a745;
                        font-size: 20px; margin-top: 20px;">
                <img src="data:image/png;base64,{icon_grand_total}" height="50" style="margin-right: 12px;" />
                <strong>Grand Total: ₹{total:.2f}</strong>
            </div>
        """, unsafe_allow_html=True)
