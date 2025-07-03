# --- 📁 file: ui_summary.py ---
import streamlit as st

def show_price_summary() -> object:
    st.subheader("✅ Step 4: Price Summary")

    attrs = st.session_state.selected_attrs
    total = 0

    if attrs:
        for label, (price, qty) in attrs.items():
            item_total = price * qty
            total += item_total
            st.markdown(
                f"<div class='card'><b>{label}</b><br>₹{price} × {qty} = ₹{item_total}</div>",
                unsafe_allow_html=True
            )
        st.markdown(
            f"<div class='card'><h4>💰 Grand Total: ₹{total}</h4></div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ No attributes were selected.")

    if st.button("🔄 Start Over"):
        for key in ["step", "categories", "varieties", "selected_attrs"]:
            del st.session_state[key]
        st.rerun()
