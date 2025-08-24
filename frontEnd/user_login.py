import streamlit as st
import requests

# Backend API base URL
API_BASE = "http://localhost:4008"  # change to your backend host if deployed

# Page config
st.set_page_config(page_title="Vendor Portal", layout="centered")
st.title("User Portal")
st.subheader("User Login")

# Login form
with st.form("login_form"):
    contact_email = st.text_input("Contact Email")
    password = st.text_input("Password", type="password")
    login_submit = st.form_submit_button("Login")

if login_submit:
    if not contact_email or not password:
        st.warning("Please enter both email and password.")
    else:
        payload = {"contact_email": contact_email, "password": password}
        with st.spinner("Logging in..."):
            try:
                response = requests.post(f"{API_BASE}/api/v1/vendor/VendorLogin", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Login Successful! Welcome {data.get('first_name', 'Vendor')}")
                else:
                    error_msg = response.json().get("error", "Invalid credentials")
                    st.error(f"Login failed: {error_msg}")
            except requests.exceptions.RequestException as e:
                st.error(f"Backend connection failed: {e}")
