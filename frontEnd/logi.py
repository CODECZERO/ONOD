import streamlit as st
import requests

# Backend API base URL
API_BASE = "http://localhost:4008"  # Change this to your backend's URL if deployed

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Vendor Portal", layout="centered")
st.title("One Nation One Document - ONOD")
st.header("Vendor Portal")

# -------------------------
# Tabs for Login and Registration
# -------------------------
tab1, tab2 = st.tabs(["Login", "Register"])

# ---------------- LOGIN ----------------
with tab1:
    st.subheader("Vendor Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")

    if login_submit:
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            payload = {"email": email, "password": password}
            try:
                response = requests.post(f"{API_BASE}/api/v1/vendore/VendeorLogin", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Login Successful! Welcome {data['data']['name']}")
                    st.json(data) # Display full response for debugging
                else:
                    st.error(f"Login failed: {response.json().get('message', 'Invalid credentials or server error')}")
            except requests.exceptions.ConnectionError:
                st.error("Connection failed. Is the backend server running?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# ---------------- REGISTRATION ----------------
with tab2:
    st.subheader("Vendor Registration")

    with st.form("register_form"):
        st.markdown("### Organisation Details")
        orgName = st.text_input("Organisation Name")
        regNo = st.text_input("Organisation Registration Number")
        orgType = st.selectbox(
            "Organisation Type",
            ["Not Selected", "Hospital", "Education", "Finance"]
        )
        
        st.markdown("### Contact Person Details")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        contact = st.text_input("Phone Number (10 digits)", max_chars=10)
        
        st.markdown("### Organisation Address")
        orgAddr = st.text_input("Full Address")
        city = st.text_input("City")
        state = st.text_input("State")
        country = st.text_input("Country", value="India")
        websiteUrl = st.text_input("Website URL")
        
        st.markdown("### Account Security")
        password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        register_submit = st.form_submit_button("Register")

        if register_submit:
            # Basic validation
            if not all([name, contact, email, orgName, regNo, orgType, orgAddr, city, state, country, password, confirm_password]):
                st.error("Please fill in all required fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif not contact.isdigit() or len(contact) != 10:
                st.error("Please enter a valid 10-digit phone number.")
            else:
                try:
                    payload = {
                        "orgName": orgName,
                        "regNo": regNo,
                        "orgType": orgType,
                        "name": name,
                        "contact": int(contact),
                        "email": email,
                        "orgAddr": orgAddr,
                        "city": city,
                        "state": state,
                        "country": country,
                        "websiteUrl": websiteUrl,
                        "password": password
                    }
                    response = requests.post(f"{API_BASE}/api/v1/vendore/vendeorReg", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Registration Successful! Your Vendor ID: {data['data'].get('uniqueID', 'N/A')}")
                        st.json(data) # Display full response for debugging
                    else:
                        st.error(f"Registration failed: {response.json().get('message', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("Connection failed. Is the backend server running?")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")