import requests

# ---------------- Config ----------------
API_BASE = "http://localhost:4008/api/v1/vendore"

# ---------------- Registration Test ----------------
register_payload = {
    "uniqueID": "test123",
    "walletId": "wallet123",
    "orgName": "Demo Organization",
    "regNo": "REG001",
    "orgType": "Private",
    "name": "John Doe",
    "contact": 9876543210,
    "email": "john@example.com",
    "orgAddr": "123 Demo Street",
    "city": "Pune",
    "state": "Maharashtra",
    "country": "India",
    "websiteUrl": "https://demo.org"
}

try:
    reg_response = requests.post(f"{API_BASE}/VendeorReg", json=register_payload)
    print("Registration Status Code:", reg_response.status_code)
    print("Registration Response:", reg_response.json())
except Exception as e:
    print("Registration request failed:", e)

# ---------------- Login Test ----------------
login_payload = {
    "email": "john@example.com",  # make sure backend expects 'email' key
    "password": "yourpassword"     # replace with actual test password
}

try:
    login_response = requests.post(f"{API_BASE}/VendeorLogin", json=login_payload)
    print("\nLogin Status Code:", login_response.status_code)
    print("Login Response:", login_response.json())
except Exception as e:
    print("Login request failed:", e)
