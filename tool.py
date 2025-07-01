import streamlit as st

# Simulated large dataset (can scale to 1000s of fields)
data = {
    "Laptop": {f"Laptop Option {i}": i * 100 for i in range(1, 101)},
    "Phone": {f"Phone Feature {i}": i * 50 for i in range(1, 201)},
    "Tablet": {f"Tablet Addon {i}": i * 75 for i in range(1, 151)},
    "Monitor": {f"Monitor Spec {i}": i * 90 for i in range(1, 121)},
    "Printer": {f"Printer Feature {i}": i * 40 for i in range(1, 81)},
    "Machine": {f"Machine Feature {i}": i * 40 for i in range(1, 81)},
}

st.set_page_config("Pricing  Tool", layout="wide")
st.title("🧾 Pricing Tool")

# --- Select Multiple Items ---
selected_items = st.multiselect("Select Items", list(data.keys()))

# --- Field selections stored dynamically ---
selected_fields = {}

if selected_items:
    st.markdown("### 🔧 Configure Fields for Each Item")

    for item in selected_items:
        with st.expander(f"Select options for: **{item}**"):
            options = list(data[item].keys())
            chosen_fields = st.multiselect(f"{item} Options", options, key=f"{item}_fields")
            if chosen_fields:
                selected_fields[item] = chosen_fields

# --- Submit Button ---
if st.button("Submit"):
    if not selected_fields:
        st.warning("Please select at least one field.")
    else:
        total_price = 0
        st.success("✅ Price Summary")

        for item, fields in selected_fields.items():
            st.markdown(f"#### 🛠️ {item}")
            item_total = sum(data[item][field] for field in fields)
            total_price += item_total
            for field in fields:
                st.write(f"✔️ {field} — ₹{data[item][field]}")

            st.markdown(f"**Subtotal for {item}: ₹{item_total}**")
            st.markdown("---")

        st.header(f"💰 Grand Total: ₹{total_price}")



