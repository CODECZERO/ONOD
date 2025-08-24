import streamlit as st

# Set page config
st.set_page_config(page_title="One Nation One ID", layout="wide")

# Custom CSS to style header
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

# Header HTML
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

st.write("## Welcome to One Nation One ID")
st.write(" ")

import streamlit as st
import urllib.parse

# Streamlit Page Config
st.set_page_config(page_title="QR Generator", page_icon="", layout="centered")

st.title("QR Code Generator")
st.write("Enter your One ID and instantly generate a QR code for it (no extra library needed).")

# User Input
user_id = st.text_input("Enter your One Nation One ID:")

# Generate QR Button
if st.button("Generate QR Code"):
    if user_id.strip() != "":
        # Encode the user_id for URL safety
        encoded_id = urllib.parse.quote(user_id)

        # Google Chart API for QR
        qr_url = f"https://chart.googleapis.com/chart?cht=qr&chs=300x300&chl={encoded_id}"

        # Display QR Code (fixed parameter)
        st.image(qr_url, caption="Your One Nation One ID QR Code", use_container_width=False)

        # Download Link
        st.markdown(
            f"[Download QR Code]({qr_url})",
            unsafe_allow_html=True
        )
    else:
        st.error("Please enter a valid ID before generating QR code.")
