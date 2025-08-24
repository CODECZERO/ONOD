# One Nation One Document (ONOD) 🆔

[![Hackathon Project](https://img.shields.io/badge/Hackathon-Winning%20Project-blue)]()
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)]()
[![Node.js](https://img.shields.io/badge/Node.js-backend-green?logo=node.js&logoColor=white)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-frontend-orange?logo=streamlit&logoColor=white)]()
[![MongoDB](https://img.shields.io/badge/MongoDB-database-green?logo=mongodb&logoColor=white)]()
[![Aptos](https://img.shields.io/badge/Blockchain-Aptos-purple)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()


## Project Overview

**One Nation One Document (ONOD)** is a **secure, unified digital identity platform** designed to streamline citizen identity and document management.  
Built as a **prototype/MVP** for hackathons, ONOD demonstrates how **blockchain technology (Aptos)** can anchor proofs securely, while the user-friendly frontend allows citizens and organizations to interact with digital records easily.

**Key Goals:**
- Simplify citizen identity management in India 🇮🇳  
- Provide tamper-proof proof generation via SHA256 + blockchain anchoring  
- Allow verified organizations to add trusted updates  
- Enable easy verification, QR-based sharing, and export options  

---

## Features

-  **Citizen Registration:** Personal info, government IDs, education, employment, and health  
-  **Secure Document Uploads:** Aadhaar, PAN, certificates, and other proofs    
-  **QR Code Generation:** Quick proof sharing and verification  
-  **Organization Portal:** Verified updates from hospitals, schools, banks, etc.  
-  **Admin Dashboard:** Inspect, export, and manage submissions  
-  **Blockchain Prototype:** Proof hashes can be anchored on Aptos for immutability  

---

## Tech Stack

| Layer           | Technology                                  |
|-----------------|--------------------------------------------|
| Frontend        | Streamlit + HTML5 + CSS3                           |
| Backend         | NodeJS + MOVE Lang                              |
| Database        | MongoDB                                     |
| Blockchain      | Aptos (Proof anchoring)                     |
| Security        | deterministic hash, for the Secure System.   |

---

## Screenshots / Demo
<img width="1855" height="945" alt="Image" src="https://github.com/user-attachments/assets/57cbdc42-64ea-407b-80f3-6745c86d8460" />

### Registration Page
<img width="1902" height="988" alt="Screenshot 2025-08-24 102943" src="https://github.com/user-attachments/assets/c83814bd-9655-4035-af6b-4318a7fd5935" />


### Citizen Dashboard
<img width="1874" height="979" alt="Screenshot 2025-08-24 103141" src="https://github.com/user-attachments/assets/2d5dc5fe-135e-4fce-9ed4-be55aeaedd66" />


### Admin / Export View
<img width="1904" height="1004" alt="Screenshot 2025-08-24 103534" src="https://github.com/user-attachments/assets/308457ae-9877-4129-877f-39fd26e6ce39" />

### Integrity Final 
<img width="1863" height="985" alt="Screenshot 2025-08-24 103759" src="https://github.com/user-attachments/assets/201c8151-915a-47a4-b6c3-1a8a4f9b000e" />


---

## Installation & Run (Local Prototype)

1. **Clone the repository**
```bash
git clone https://github.com/CODECZERO/one-nation-one-document.git
cd one-nation-one-document



2. Install backend dependencies
cd backend 
npm install


3. Install frontend dependencies
cd ./frontend
pip install -r requirements.txt


4. Run backend
node server.js


5. Run frontend
streamlit run app.py


6. Open http://localhost:8501 to view the application.

---

 Project Reference:

Blockchain Reference (Aptos): https://aptoslabs.com

Frontend Repo: ./frontend

Backend Repo: ./backend


Usage:
- Register a citizen profile with personal, government, education, and employment info.
- Upload supporting documents (Aadhaar, PAN, certificates, etc.).
- Generate a deterministic SHA256 proof hash and optionally anchor on Aptos.
- Admins can view, verify, and export submissions.
- Organizations can add verified updates.
- QR codes enable quick proof verification offline or online.


Hackathon Highlights:
- Prototype MVP ready in < 24 hours
- Secure, blockchain-backed digital identity demo.
- Innovative QR + proof hash verification
- Easy integration for organizations and admins
- Highly scalable architecture using NodeJS + MongoDB + Aptos

License
MIT License 

