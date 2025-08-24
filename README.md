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

- ✅ **Citizen Registration:** Personal info, government IDs, education, employment, and health  
- ✅ **Secure Document Uploads:** Aadhaar, PAN, certificates, and other proofs  
- ✅ **Proof Hash Generation:** Deterministic SHA256 hash for each submission  
- ✅ **QR Code Generation:** Quick proof sharing and verification  
- ✅ **Organization Portal:** Verified updates from hospitals, schools, banks, etc.  
- ✅ **Admin Dashboard:** Inspect, export, and manage submissions  
- ✅ **Blockchain Prototype:** Proof hashes can be anchored on Aptos for immutability  

---

## Tech Stack

| Layer           | Technology                                  |
|-----------------|--------------------------------------------|
| Frontend        | Streamlit + CSS                             |
| Backend         | NodeJS + MOVE                               |
| Database        | MongoDB                                     |
| Blockchain      | Aptos (Proof anchoring)                     |
| Security        | SHA256 deterministic hash, QR code proofs   |

---

## Screenshots / Demo

### Registration Page
![Registration Page](./screenshots/registration.png)

### Citizen Dashboard
![Dashboard](./screenshots/dashboard.png)

### Admin / Export View
![Admin Dashboard](./screenshots/admin.png)

> Replace with actual screenshots or GIFs of your app.

---

## Installation & Run (Local Prototype)

1. **Clone the repository**
```bash
git clone https://github.com/your-username/one-nation-one-document.git
cd one-nation-one-document
2. **Install backend dependencies**
cd backend
npm install
3. **Install frontend dependencies**
cd ../frontend
pip install -r requirements.txt
4. **Run backend**
node server.js
5. **Run frontend**
streamlit run app.py
6. Open http://localhost:8501 to view the application.

---

**Usage**
- Register a citizen profile with personal, government, education, and employment info.
- Upload supporting documents (Aadhaar, PAN, certificates, etc.).
- Generate a deterministic SHA256 proof hash and optionally anchor on Aptos.
- Admins can view, verify, and export submissions.
- Organizations can add verified updates.
- QR codes enable quick proof verification offline or online.

**Team ONOD – Hackathon Participants**
| Name           | Role                   | Contact                                                       |
| -------------- | ---------------------- | ------------------------------------------------------------- |
| Harish Jagdale | Full-stack Developer   | [harish.email@example.com](mailto:harish.email@example.com)   |
| Member 2       | Blockchain Developer   | [member2.email@example.com](mailto:member2.email@example.com) |
| Member 3       | Frontend & UX Designer | [member3.email@example.com](mailto:member3.email@example.com) |

Hackathon Highlights
- Prototype MVP ready in < 24 hours
- Secure, blockchain-backed digital identity demo
- Innovative QR + proof hash verification
- Easy integration for organizations and admins
- Highly scalable architecture using NodeJS + MongoDB + Aptos

License
MIT License © 2025 Harish Jagdale

Acknowledgements
- Inspired by government digital identity initiatives
- Built with Streamlit
, Node.js
, MongoDB
, and Aptos
