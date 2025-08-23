import requests

# API endpoint (change port if needed, e.g. 3000)
url = "http://127.0.0.1:4008/api/v1/vendore/issue"

# Example BlockDataTS payload
payload = {
    "issuer": "0x8d8582b439da550184762571254cae02f227b5e09ee2626ae6fa0dff8b791cd7",
    "receiver": "0xf2099e52f02e834476b3463f092c20efadbb69f9a6da0748b0dc3623ba7bcbdd",
    "docType": "Certificate",
    "docId": "CERT-2025-001",
    "metaData": {
        "name": "Ankit Singh Mahar",
        "course": "Blockchain Development",
        "grade": "A+",
        "issuedOn": "2025-08-23"
    },
    "chain": ["step1", "step2", "step3"]
}

# Send POST request
try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)
