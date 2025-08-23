import streamlit as st
import requests

# Backend API base URL
API_BASE = "http://localhost:4008"  # change to your backend host if deployed

# Page Config
st.set_page_config(page_title="Vendor Registration", layout="centered")

st.title("Vendor Registration")

# Registration Form
with st.form("register_form"):
    org_name = st.text_input("Organization Name")
    reg_no = st.text_input("Registration Number")
    org_type = st.text_input("Organization Type")
    org_subtype = st.text_input("Organization Subtype")
    first_name = st.text_input("Contact Person First Name")
    middle_name = st.text_input("Contact Person Middle Name")
    last_name = st.text_input("Contact Person Last Name")
    contact_email = st.text_input("Contact Email")
    password = st.text_input("Password", type="password")
    org_email = st.text_input("Organization Email")
    org_phone = st.text_input("Organization Phone Number")
    org_address = st.text_input("Organization Address")
    city = st.text_input("City")
    state = st.text_input("State")
    country = st.text_input("Country")
    pincode = st.text_input("Pincode")
    website = st.text_input("Website URL")

    register_submit = st.form_submit_button("Register")

# Handle Submit
if register_submit:
    payload = {
        "org_name": org_name,
        "reg_no": reg_no,
        "org_type": org_type,
        "org_subtype": org_subtype,
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "contact_email": contact_email,
        "password": password,
        "org_email": org_email,
        "org_phone": org_phone,
        "org_address": org_address,
        "city": city,
        "state": state,
        "country": country,
        "pincode": pincode,
        "website": website
    }

    try:
        response = requests.post(f"{API_BASE}/api/v1/vendore/VendeorReg", json=payload)

        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ Registration Successful! Your Vendor ID: {data.get('vendorId', 'N/A')}")
        else:
            st.error(response.json().get("error", "Registration failed"))
    except Exception as e:
        st.error(f"⚠️ Backend connection failed: {e}")

# Footer
st.markdown("---")
st.markdown("Already registered?")
st.page_link("Home.py", label="Login Here", icon="🔑")
