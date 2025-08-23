import streamlit as st
import requests

# Backend API base URL
API_BASE = "http://localhost:4008"  # change to your backend host if deployed

# Page config
st.set_page_config(page_title="Vendor Portal", layout="centered")
st.title(" Vendor Portal")

# Tabs for Login and Registration
tab1, tab2 = st.tabs(["Login", "Register"])

# ---------------- LOGIN ----------------
with tab1:
    st.subheader("Vendor Login")

    with st.form("login_form"):
        contact_email = st.text_input("Contact Email")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")

    if login_submit:
        payload = {"contact_email": contact_email, "password": password}
        try:
            response = requests.post(f"{API_BASE}/api/v1/vendore/VendeorLogin", json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Login Successful! Welcome {data.get('first_name', 'Vendor')}")
            else:
                st.error(response.json().get("error", "Invalid credentials"))
        except Exception as e:
            st.error(f" Backend connection failed: {e}")

# ---------------- REGISTRATION ----------------
with tab2:
    st.subheader("Vendor Registration")

    with st.form("register_form"):

        name = st.text_input("Full Name (Contact Person)")
        contact = st.text_input("Phone Number (Contact Person)")
        email = st.text_input("Email (Contact Person)")
        orgName = st.text_input("Organisation Name")
        regNo = st.text_input("Organisation Registration Number")
        
        # Dropdown for Organization Type
        orgType = st.selectbox(
            "Organisation Type",
            ["Not Selected", "Hospital", "Education", "Finance"]
        )
        contact = st.text_input("Organisation Phone Number")
        email = st.text_input("Organisation Email")
        orgAddr = st.text_input("Organisation Address")
        city = st.text_input("City")
        state = st.text_input("State")
        country = st.text_input("Country")
        websiteUrl = st.text_input("Website URL")

        register_submit = st.form_submit_button("Register")

        if register_submit:
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
                "websiteUrl": websiteUrl
            }

            try:
                response = requests.post(f"{API_BASE}/api/v1/vendore/VendeorReg", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Registration Successful! Your Vendor ID: {data.get('vendorId', 'N/A')}")
                else:
                    st.error(response.json().get("error", "Registration failed"))
            except Exception as e:
                st.error(f" Backend connection failed: {e}")
