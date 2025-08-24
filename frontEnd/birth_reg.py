import streamlit as st
import uuid
from datetime import date

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="One Nation One Document - ONOD", layout="wide")


# -------------------------
# Custom CSS for Center Alignment
# -------------------------
st.markdown("""
    <style>
    .stApp {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .centered-title {
        text-align: center;
    }
    .centered-form {
        width: 600px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# In-memory data store
# -------------------------
if "registered_babies" not in st.session_state:
    st.session_state.registered_babies = []

# -------------------------
# Function to generate Unique ID
# -------------------------
def generate_unique_id():
    return "ONOID-" + str(uuid.uuid4())[:8].upper()

# -------------------------
# Centered Title
# -------------------------
st.markdown('<h1 class="centered-title">One Nation One Document - ONOD</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="centered-title">Birth Registration</h3>', unsafe_allow_html=True)

# -------------------------
# Registration Form (Centered)
# -------------------------
with st.form("baby_registration_form", clear_on_submit=True):
        baby_first_name = st.text_input("First Name", placeholder="Enter first name")
        baby_last_name = st.text_input("Last Name", placeholder="Enter last name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        birth_date = st.date_input("Date of Birth", value=date.today())
        time_of_birth = st.text_input("Time of Birth", placeholder="HH:MM")
        place_of_birth = st.text_input("Place of Birth")
        father_name = st.text_input("Father's Full Name")
        father_id = st.text_input("Father ID")
        father_contact = st.text_input("Father Contact Number", max_chars=10, placeholder="10-digit number")
        father_email = st.text_input("Father Email")
        mother_name = st.text_input("Mother's Full Name")
        mother_id = st.text_input("Mother ID")
        mother_contact = st.text_input("Mother Contact Number", max_chars=10, placeholder="10-digit number")
        mother_email = st.text_input("Mother Email")
        address_line = st.text_area("Full Address")
        city = st.text_input("City")
        state = st.text_input("State")
        country = st.text_input("Country", value="India")
        
        submitted = st.form_submit_button("Register")

        if submitted:
            required_fields = [
                baby_first_name, baby_last_name, gender, birth_date, time_of_birth, place_of_birth,
                father_name, father_id, father_contact, father_email,
                mother_name, mother_id, mother_contact, mother_email,
                address_line, city, state, country
            ]
            if not all(required_fields):
                st.error("Please fill in all required fields.")
            else:
                unique_id = generate_unique_id()
                baby_record = {
                    "Unique ID": unique_id,
                    "Baby Name": f"{baby_first_name} {baby_last_name}",
                    "Gender": gender,
                    "Birth Date": str(birth_date),
                    "Time of Birth": time_of_birth,
                    "Place of Birth": place_of_birth,
                    "Father Name": father_name,
                    "Father ID": father_id,
                    "Father Contact": father_contact,
                    "Father Email": father_email,
                    "Mother Name": mother_name,
                    "Mother ID": mother_id,
                    "Mother Contact": mother_contact,
                    "Mother Email": mother_email,
                    "Address": address_line,
                    "City": city,
                    "State": state,
                    "Country": country
                }
                st.session_state.registered_babies.append(baby_record)
                st.success(f"Newborn registered successfully! Unique One Nation One ID: **{unique_id}**")

# -------------------------
# Display Registered Babies
# -------------------------
if st.session_state.registered_babies:
    st.subheader("Registered Newborn Records")
    for baby in st.session_state.registered_babies:
        with st.expander(f"{baby['Baby Name']} - {baby['Unique ID']}"):
            st.write(f"**Gender:** {baby['Gender']}")
            st.write(f"**Birth Date:** {baby['Birth Date']}")
            st.write(f"**Time of Birth:** {baby['Time of Birth']}")
            st.write(f"**Place of Birth:** {baby['Place of Birth']}")
            st.write(f"**Father Name:** {baby['Father Name']}")
            st.write(f"**Father ID:** {baby['Father ID']}")
            st.write(f"**Father Contact:** {baby['Father Contact']}")
            st.write(f"**Father Email:** {baby['Father Email']}")
            st.write(f"**Mother Name:** {baby['Mother Name']}")
            st.write(f"**Mother ID:** {baby['Mother ID']}")
            st.write(f"**Mother Contact:** {baby['Mother Contact']}")
            st.write(f"**Mother Email:** {baby['Mother Email']}")
            st.write(f"**Address:** {baby['Address']}, {baby['City']}, {baby['State']}, {baby['Country']}")
