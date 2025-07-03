import streamlit as st
import base64

# --- Helper to load icons as Base64 ---
import os

def load_icon(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    else:
        st.warning(f"⚠️ File not found: {path}")
        return ""


# --- Load all icons ---
icon_app = load_icon("img1.png")
icon_seg = load_icon("img2.png")
icon_mach = load_icon("machine.png")
icon_mesh = load_icon("mesh-micro.png")
icon_white = load_icon("whiteness.png")
icon_kg = load_icon("weight.png")
icon_type = load_icon("category.png")

# --- CSS Styling ---
st.set_page_config(layout="wide", page_title="Pricing Tool")

st.markdown("""
    <style>
        .main > div:first-child {
            padding-top: 30px !important;
            margin-top: 0px !important;
        }

        .after-title-gap {
            margin-top: 40px;
        }

        .stApp {
            padding-left: 5vw;
            padding-right: 5vw;
            max-width: 2400px;
            margin: auto;
        }

        .qty-box {
            text-align: center;
            padding: 6px 12px;
            background-color: #f5f5f5;
            border-radius: 8px;
            display: inline-block;
            min-width: 45px;
            font-weight: bold;
            font-size: 16px;
        }

        .icon-title {
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 26px;
            font-weight: 600;
            margin-bottom: 10px;
            margin-top: 20px;
        }

        .icon-title img {
            height: 42px;
            width: auto;
        }

        .stMultiSelect:hover {
            transform: scale(1.01);
            transition: 0.2s ease-in-out;
        }

        .golcha-logo-wrapper {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-top: 10px;  
        }

        .golcha-logo-wrapper img {
            height: 100px;  
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
       }

       .golcha-logo-wrapper h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 700;
       }

    </style>
""", unsafe_allow_html=True)


# --- Catalog ---
catalog = {
    "Applications": {"ABC": 100, "DEF": 150, "XYZ": 120, "LMN": 110, "PQR": 130, "TUV": 160, "GHI": 170},
    "Segment": {"Industrial": 300, "Food Grade": 450, "Pharma": 600, "Mining": 400},
    "Machine": {"M1": 1000, "M2": 1200, "M3": 900, "M4": 300},
    "Mesh/Micro": {"150 Mesh": 150, "200 Mesh": 180, "300 Mesh": 210, "400 Mesh": 250},
    "Whiteness": {"Standard": 50, "High": 80, "Ultra": 120, "Super High": 180},
    "Packing > KG": {"25 KG": 25, "50 KG": 40, "75 KG": 75, "100 KG": 100},
    "Packing > Type": {"HDPE": 10, "Paper Bag": 15, "Jumbo Bag": 30, "Plastic Bag": 40}
}

# --- Session Init ---
if "qty_state" not in st.session_state:
    st.session_state.qty_state = {}

# --- Sidebar Navigation ---
page = st.sidebar.radio("🔘 Navigate", ["🏠 Home", "📦 Price Calculator"])

# ------------------ HOME ------------------
if page == "🏠 Home":
    import os

    logo_path = "D:/Pricing tool/icons/Golcha-Logo.png"
    if os.path.exists(logo_path):
        encoded_logo = base64.b64encode(open(logo_path, "rb").read()).decode()
        logo_html = f"""
            <div class="golcha-logo-wrapper">
                <h1>🏠 Welcome to the Pricing Tool</h1>
                <img src="data:image/png;base64,{encoded_logo}" alt="Golcha Logo">
            </div>
        """
    else:
        logo_html = "<h1>🏠 Welcome to the Pricing Tool</h1><p style='color: red;'>⚠️ Logo not found</p>"

    st.markdown(logo_html, unsafe_allow_html=True)
    st.markdown('<div class="after-title-gap"></div>', unsafe_allow_html=True)

    st.markdown("""
        This is a **multi-level, dynamic pricing calculator** for your business needs.

        ### 💡 Features:
        - 🔻 Expand/collapse input categories  
        - ➕➖ Quantity controls  
        - 📦 Multi-field selection  
        - 💰 Calculate total cost  
    """)


# ------------------ PRICING TOOL ------------------
elif page == "📦 Price Calculator":
    import os

    logo_path = "D:/Pricing tool/icons/Golcha-Logo.png"
    if os.path.exists(logo_path):
        encoded_logo = base64.b64encode(open(logo_path, "rb").read()).decode()
        logo_html = f"""
            <div class="golcha-logo-wrapper">
                <h1>📦 Pricing Tool</h1>
                <img src="data:image/png;base64,{encoded_logo}" alt="Golcha Logo">
            </div>
        """
    else:
        logo_html = "<h1>📦 Pricing Tool</h1><p style='color: red;'>⚠️ Logo not found</p>"

    st.markdown(logo_html, unsafe_allow_html=True)
    st.markdown('<div class="after-title-gap"></div>', unsafe_allow_html=True)

    # --- Reset Function ---
    def reset_all():
        st.session_state.qty_state = {}
        for key in list(st.session_state.keys()):
            if key.endswith("_select"):
                st.session_state[key] = []

    # --- Reset Button ---
    if st.button("🧹 Reset Selections", key="reset_button"):
        reset_all()
        st.experimental_rerun()

    # Continue with your calculator logic...

    # --- Section Renderer ---
    selected_items = {}


    def render_section(title, options_dict, key_prefix="", icon=None):
        st.markdown(f"""
            <div class="icon-title">
                <img src="data:image/png;base64,{icon}" />
                <span>{title}</span>
            </div>
        """, unsafe_allow_html=True)

        selections = st.multiselect(
            label="",
            options=list(options_dict.keys()),
            key=f"{key_prefix}_select",
            placeholder=f"🔍 Search {title}"
        )

        for opt in selections:
            state_key = f"{key_prefix}_{opt}_qty"
            if state_key not in st.session_state.qty_state:
                st.session_state.qty_state[state_key] = 1

            col1, col2, col3, col4 = st.columns([2.5, 1, 1, 2.5])
            with col1:
                st.markdown(f"**{opt}** — ₹{options_dict[opt]}")
            with col2:
                if st.button("➖", key=f"{state_key}_dec") and st.session_state.qty_state[state_key] > 1:
                    st.session_state.qty_state[state_key] -= 1
            with col3:
                st.markdown(f"<div class='qty-box'>{st.session_state.qty_state[state_key]}</div>",
                            unsafe_allow_html=True)
            with col4:
                if st.button("➕", key=f"{state_key}_inc"):
                    st.session_state.qty_state[state_key] += 1

            selected_items[f"{title} > {opt}"] = (options_dict[opt], st.session_state.qty_state[state_key])


    # --- Sections ---
    st.markdown("### 🧩 Applications & Segment")
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        render_section("Applications", catalog["Applications"], key_prefix="app", icon=icon_app)
    with col2:
        render_section("Segment", catalog["Segment"], key_prefix="seg", icon=icon_seg)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Machine, Mesh & Whiteness")
    col3, col4, col5 = st.columns([1, 1, 1], gap="large")
    with col3:
        render_section("Machine", catalog["Machine"], key_prefix="mach", icon=icon_mach)
    with col4:
        render_section("Mesh/Micro", catalog["Mesh/Micro"], key_prefix="mesh", icon=icon_mesh)
    with col5:
        render_section("Whiteness", catalog["Whiteness"], key_prefix="white", icon=icon_white)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("### 📦 Packing")
    col6, col7 = st.columns([1, 1], gap="large")
    with col6:
        render_section("Packing > KG", catalog["Packing > KG"], key_prefix="kg", icon=icon_kg)
    with col7:
        render_section("Packing > Type", catalog["Packing > Type"], key_prefix="ptype", icon=icon_type)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Calculate Button & Summary ---
    if st.button("💰 Calculate Total", key="calc_total"):
        if selected_items:
            total = 0
            st.subheader("🧾 Price Summary")
            for name, (price, qty) in selected_items.items():
                subtotal = price * qty
                total += subtotal
                st.markdown(f"- **{name}**: ₹{price} × {qty} = ₹{subtotal}")
            st.success(f"### ✅ Grand Total: ₹{total}")
        else:
            st.warning("⚠️ Please select at least one option.")

    # --- Recent Selections AFTER total ---
    if selected_items:
        st.markdown("#### 🕓 Recent Selections")
        for name, (price, qty) in selected_items.items():
            st.markdown(f"- **{name}**: ₹{price} × {qty}")



