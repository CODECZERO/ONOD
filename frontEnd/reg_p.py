import streamlit as st
import requests

# Backend API base URL
API_BASE = "http://localhost:4008"  # change to your backend host if deployed

# Page config
st.set_page_config(page_title="One Nation One ID - Vendor Portal", layout="wide")

# ---------------- Header ----------------
st.markdown("""
    <style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 25px;
        background-color: white;
        border-bottom: 1px solid #ddd;
    }
    .header-logo img {
        height: 40px;
    }
    .header-user img {
        height: 40px;
        border-radius: 50%;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-logo">
        <img src="https://www.mygov.in/sites/all/themes/mygov/images/logo.png" alt="MyGov Logo">
    </div>
    <div class="header-user">
        <img src="https://cdn-icons-png.flaticon.com/512/847/847969.png" alt="User Icon">
    </div>
</div>
""", unsafe_allow_html=True)

st.write("## Welcome to One Nation One ID Vendor Portal")
st.write(" ")

# ---------------- Tabs ----------------
tab1, tab2 = st.tabs(["Login", "Register"])

# ---------------- LOGIN ----------------
with tab1:
    st.subheader("Vendor Login")

    with st.form("login_form"):
        contact_email = st.text_input("Contact Email")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")

    if login_submit:
        if not contact_email or not password:
            st.warning("Please enter both email and password.")
        else:
            payload = {"contact_email": contact_email, "password": password}
            try:
                response = requests.post(f"{API_BASE}/api/v1/vendor/VendorLogin", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Login Successful! Welcome {data.get('first_name', 'Vendor')}")
                else:
                    st.error(response.json().get("error", "Invalid credentials"))
            except requests.exceptions.RequestException as e:
                st.error(f"Backend connection failed: {e}")

# ---------------- REGISTRATION ----------------
with tab2:
    st.subheader("Vendor Registration")

    with st.form("register_form"):

        # Contact person info
        name = st.text_input("Full Name (Contact Person)")
        contact_person = st.text_input("Phone Number (Contact Person)")
        email_person = st.text_input("Email (Contact Person)")

        # Organization info
        org_name = st.text_input("Organisation Name")
        reg_no = st.text_input("Organisation Registration Number")
        org_type = st.selectbox(
            "Organisation Type",
            ["Not Selected", "Hospital", "Education", "Finance"]
        )
        contact_org = st.text_input("Organisation Phone Number")
        email_org = st.text_input("Organisation Email")
        org_addr = st.text_input("Organisation Address")
        city = st.text_input("City")
        state = st.text_input("State")
        country = st.text_input("Country")
        website_url = st.text_input("Website URL")

        register_submit = st.form_submit_button("Register")

        if register_submit:
            # Optional IDs if not available
            uniqueID = None
            walletId = None

            # Validate required fields
            if not (name and contact_person and email_person and org_name and org_type != "Not Selected"):
                st.warning("Please fill all required fields and select Organisation Type.")
            else:
                payload = {
                    "uniqueID": uniqueID,
                    "walletId": walletId,
                    "orgName": org_name,
                    "regNo": reg_no,
                    "orgType": org_type,
                    "name": name,
                    "contact": contact_person,
                    "email": email_person,
                    "orgAddr": org_addr,
                    "city": city,
                    "state": state,
                    "country": country,
                    "websiteUrl": website_url
                }

                try:
                    response = requests.post(f"{API_BASE}/api/v1/vendor/VendorReg", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Registration Successful! Your Vendor ID: {data.get('vendorId', 'N/A')}")
                    else:
                        st.error(response.json().get("error", "Registration failed"))
                except requests.exceptions.RequestException as e:
                    st.error(f"Backend connection failed: {e}")
