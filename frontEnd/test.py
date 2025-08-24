import requests
import json
import random
import string
import time

# Base URL of your Express.js server
BASE_URL = "http://localhost:4008/api/v1/vendore"

def generate_random_string(length=8):
    """Generate a random string of letters and digits."""
    letters_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_digits) for i in range(length))

def test_vendor_registration(email_suffix):
    """Test the /vendeorReg endpoint."""
    print(f"--- Testing /vendeorReg with email: {email_suffix} ---")
    
    payload = {
        "password": "password123",
        "orgName": f"Org_{generate_random_string()}",
        "regNo": str(random.randint(10000, 99999)),
        "orgType": "Private",
        "name": f"Test User {email_suffix}",
        "contact": int(f"987{random.randint(1000000, 9999999)}"),
        "email": f"test.user.{email_suffix}@example.com",
        "orgAddr": "123 Main St",
        "city": "TestCity",
        "state": "TestState",
        "country": "TestCountry",
        "websiteUrl": "http://test.com"
    }

    try:
        response = requests.post(f"{BASE_URL}/vendeorReg", json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        print("Registration successful!")
        print(f"Status Code: {response.status_code}")
        print("Response Data:", json.dumps(data, indent=2))
        
        # Extract and return the uniqueID for the next test
        vendor_info = data.get("data")
        if vendor_info and "uniqueID" in vendor_info:
            return vendor_info
        else:
            raise ValueError("Failed to retrieve uniqueID from registration response.")

    except requests.exceptions.RequestException as e:
        print(f"Error during registration: {e}")
        return None

def test_data_issuance(issuer_id, receiver_id):
    """Test the /issue endpoint."""
    print("\n--- Testing /issue endpoint ---")

    payload = {
        "issuer": issuer_id,
        "receiver": receiver_id,
        "docType": "Certificate",
        "docId": f"DOC-{int(time.time())}",
        "metaData": {
            "title": "Aptos Development Certificate",
            "date": "2025-08-24",
            "issuer_name": "Test Academy"
        },
        "chain": ["test_chain_v1"]
    }

    try:
        response = requests.post(f"{BASE_URL}/issue", json=payload)
        response.raise_for_status()
        
        data = response.json()
        print("Issuance successful!")
        print(f"Status Code: {response.status_code}")
        print("Response Data:", json.dumps(data, indent=2))
        
        # Extract and return the transaction ID for the next test
        vendor_data = data.get("data")
        if vendor_data and "transId" in vendor_data:
            return vendor_data["transId"][0]
        else:
            raise ValueError("Failed to retrieve transaction ID from issuance response.")

    except requests.exceptions.RequestException as e:
        print(f"Error during data issuance: {e}")
        return None

def test_read_transaction(trans_id):
    """Test the /readData endpoint."""
    print("\n--- Testing /readData endpoint ---")
    
    # Note: The Express code uses a GET method but expects a JSON body,
    # which is not standard for GET. We will send it as a POST
    # request to match the server-side implementation.
    payload = {"transId": trans_id}

    try:
        response = requests.post(f"{BASE_URL}/readData", json=payload)
        response.raise_for_status()
        
        data = response.json()
        print("Transaction read successful!")
        print(f"Status Code: {response.status_code}")
        print("Response Data:", json.dumps(data, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Error reading transaction: {e}")

if __name__ == "__main__":
    
    # Step 1: Register two vendors
    issuer_vendor = test_vendor_registration("issuer")
    if not issuer_vendor:
        print("Failed to register issuer. Exiting.")
    else:
        time.sleep(1) # Small delay for separation
        receiver_vendor = test_vendor_registration("receiver")
        
        if not receiver_vendor:
            print("Failed to register receiver. Exiting.")
        else:
            # Step 2: Issue data using the two vendors' uniqueIDs
            issuer_unique_id = issuer_vendor["uniqueID"]
            receiver_unique_id = receiver_vendor["uniqueID"]
            
            transaction_id = test_data_issuance(issuer_unique_id, receiver_unique_id)
            
            if transaction_id:
                # Step 3: Read the transaction
                test_read_transaction(transaction_id)
            else:
                print("Failed to get transaction ID. Cannot test reading data.")