import streamlit as st
import requests

# Backend API URL
API_BASE = "http://localhost:4008"  # change when deployed

st.set_page_config(page_title="Vendor Registration", layout="centered")
st.title("Vendor Registration")

with st.form("register_form"):
    org_name = st.text_input("Organization Name")
    reg_no = st.text_input("Registration Number")
    org_type = st.text_input("Organization Type")
    org_subtype = st.text_input("Organization Subtype")
    first_name = st.text_input("Contact Person First Name")
    middle_name = st.text_input("Contact Person Middle Name")
    last_name = st.text_input("Contact Person Last Name")
    contact_email = st.text_input("Contact Email ID")
    password = st.text_input("Password", type="password")
    org_email = st.text_input("Organization Email ID")
    org_phone = st.text_input("Organization Phone Number")
    org_address = st.text_input("Organization Address")
    city = st.text_input("City")
    state = st.text_input("State")
    country = st.text_input("Country")
    pincode = st.text_input("Pincode")
    website = st.text_input("Website URL")

    register_submit = st.form_submit_button("Register")

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
        "website": website,
    }

    try:
        response = requests.post(f"{API_BASE}/api/v1/vendore/VendeorReg", json=payload)

        if response.status_code == 200:
            data = response.json()
            vendor_id = data.get("vendorId") or data.get("walletId") or "N/A"
            st.success(f"Registration Successful! Your Vendor ID: {vendor_id}")
        else:
            st.error(response.json().get("error", " Registration failed"))
    except Exception as e:
        st.error(f" Could not connect to backend: {e}")

st.markdown("---")
st.markdown("Already have an account?")
st.page_link("login.py", label="Login Here")
