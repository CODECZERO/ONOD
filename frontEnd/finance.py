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

import os
import json
import sqlite3
import hashlib
from datetime import datetime
from decimal import Decimal

import streamlit as st
import pandas as pd

# ---------- Configuration ----------
DB_PATH = "finance_lifecycle.db"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Database helpers ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            full_name TEXT,
            dob TEXT,
            dod TEXT,
            personal JSON,
            birth_doc_path TEXT,
            education JSON,
            employment JSON,
            bank_accounts JSON,
            investments JSON,
            insurance JSON,
            taxes JSON,
            will JSON,
            death_doc_path TEXT,
            proof_hash TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def save_uploaded_file(uploaded_file, category, submission_id=None):
    """Save uploaded file to disk and return saved path."""
    if not uploaded_file:
        return None
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    name = uploaded_file.name
    safe_name = f"{category}_{ts}_{name}"
    path = os.path.join(UPLOAD_DIR, safe_name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def save_submission(record: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO submissions (
            created_at, full_name, dob, dod, personal, birth_doc_path,
            education, employment, bank_accounts, investments, insurance, taxes, will, death_doc_path, proof_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record.get("created_at"),
            record.get("full_name"),
            record.get("dob"),
            record.get("dod"),
            json.dumps(record.get("personal", {})),
            record.get("birth_doc_path"),
            json.dumps(record.get("education", {})),
            json.dumps(record.get("employment", {})),
            json.dumps(record.get("bank_accounts", {})),
            json.dumps(record.get("investments", {})),
            json.dumps(record.get("insurance", {})),
            json.dumps(record.get("taxes", {})),
            json.dumps(record.get("will", {})),
            record.get("death_doc_path"),
            record.get("proof_hash"),
        ),
    )
    conn.commit()
    conn.close()

def get_all_submissions_df():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM submissions ORDER BY id DESC", conn)
    conn.close()
    return df

# ---------- Utilities ----------
def compute_proof_hash(data: dict) -> str:
    """
    Compute SHA256 hex digest of sorted JSON (deterministic).
    Use this hex as a verifiable proof to anchor on-chain or on IPFS.
    """
    s = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def safe_decimal(x):
    try:
        return float(Decimal(x))
    except Exception:
        return 0.0

# ---------- App UI ----------
st.set_page_config(page_title="One Nation — Finance Lifecycle", layout="wide", page_icon="💳")
st.title("One Nation — Finance: Full Lifecycle Data Collector")
st.write("Collect finance-related documents and structured data from birth → death. "
         "This app stores metadata locally (SQLite) and files under `./uploads/`. "
         "It can compute a SHA256 proof hash for each submission to anchor on-chain or store on IPFS.")

init_db()

# --- Main Form ---
st.header("New Submission — Birth → Death Financial Record")
with st.form("lifecycle_form", clear_on_submit=False):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Personal & Birth")
        full_name = st.text_input("Full name", "")
        dob = st.date_input("Date of birth (DOB)", value=None)
        gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
        place_of_birth = st.text_input("Place of birth (city, state, country)")
        birth_doc = st.file_uploader("Upload Birth Certificate (optional)", type=["pdf", "png", "jpg", "jpeg"])

        st.subheader("Education (structured)")
        # Provide up to three major entries (school, UG, PG)
        education_entries = []
        for level in ["School (1-12)", "Undergraduate (UG)", "Postgraduate (PG) / Diploma"]:
            with st.expander(f"{level} details", expanded=False):
                inst = st.text_input(f"{level} - Institution name", key=f"edu_{level}_inst")
                degree = st.text_input(f"{level} - Degree / Stream", key=f"edu_{level}_degree")
                passing_year = st.text_input(f"{level} - Passing year", key=f"edu_{level}_year")
                score = st.text_input(f"{level} - Percentage / CGPA", key=f"edu_{level}_score")
                if inst or degree or passing_year:
                    education_entries.append({
                        "level": level,
                        "institution": inst,
                        "degree": degree,
                        "passing_year": passing_year,
                        "score": score
                    })

        st.subheader("Employment & Career")
        employment_entries = []
        add_job_count = st.number_input("Number of previous jobs to add (0-5)", min_value=0, max_value=10, value=0)
        for i in range(int(add_job_count)):
            with st.expander(f"Job #{i+1}"):
                org = st.text_input(f"Employer name #{i+1}", key=f"job_org_{i}")
                role = st.text_input(f"Role / Title #{i+1}", key=f"job_role_{i}")
                start = st.date_input(f"Start date #{i+1}", key=f"job_start_{i}")
                end = st.date_input(f"End date #{i+1} (or same as start)", key=f"job_end_{i}")
                salary = st.number_input(f"Last drawn annual salary (INR) #{i+1}", min_value=0.0, key=f"job_salary_{i}")
                employment_entries.append({
                    "employer": org,
                    "role": role,
                    "start": str(start),
                    "end": str(end),
                    "salary": safe_decimal(salary),
                })

    with col2:
        st.subheader("Financial Accounts")
        st.markdown("Add bank accounts, cards and basic KYC doc (no sensitive details required here).")
        bank_accounts = []
        add_bank_count = st.number_input("Number of bank accounts to add (0-5)", min_value=0, max_value=10, value=0, key="bank_count")
        for i in range(int(add_bank_count)):
            with st.expander(f"Bank account #{i+1}"):
                bank_name = st.text_input(f"Bank name #{i+1}", key=f"bank_name_{i}")
                acc_type = st.selectbox(f"Account type #{i+1}", ["Savings", "Current", "NRI", "Other"], key=f"bank_type_{i}")
                ifsc = st.text_input(f"IFSC / Branch (optional) #{i+1}", key=f"bank_ifsc_{i}")
                bank_accounts.append({"bank": bank_name, "type": acc_type, "ifsc": ifsc})

        st.subheader("Investments & Assets")
        investments = []
        add_inv_count = st.number_input("Number of investment entries to add (0-10)", min_value=0, max_value=10, value=0, key="inv_count")
        for i in range(int(add_inv_count)):
            with st.expander(f"Investment #{i+1}"):
                itype = st.selectbox(f"Type #{i+1}", ["Stocks", "Mutual Funds", "Fixed Deposit", "Real Estate", "Crypto", "Other"], key=f"inv_type_{i}")
                name = st.text_input(f"Name / Identifier #{i+1}", key=f"inv_name_{i}")
                amount = st.number_input(f"Amount invested / current value (INR) #{i+1}", min_value=0.0, key=f"inv_amount_{i}")
                investments.append({"type": itype, "name": name, "value_inr": safe_decimal(amount)})

        st.subheader("Insurance & Pensions")
        insurance_entries = []
        add_ins_count = st.number_input("Number of insurance/pension policies to add (0-5)", min_value=0, max_value=10, value=0, key="ins_count")
        for i in range(int(add_ins_count)):
            with st.expander(f"Policy #{i+1}"):
                provider = st.text_input(f"Provider #{i+1}", key=f"ins_provider_{i}")
                policy_no = st.text_input(f"Policy No #{i+1}", key=f"ins_no_{i}")
                sum_assured = st.number_input(f"Sum assured (INR) #{i+1}", min_value=0.0, key=f"ins_sum_{i}")
                insurance_entries.append({"provider": provider, "policy_no": policy_no, "sum_assured": safe_decimal(sum_assured)})

        st.subheader("Taxes & Documents")
        st.text_input("PAN / Tax ID (optional)", key="tax_pan")
        st.file_uploader("Upload tax documents (1 or more)", accept_multiple_files=True, key="tax_docs")

    st.markdown("---")
    st.subheader("End-of-life & Will")
    will_exists = st.checkbox("Do you have a Will / Nomination recorded?", value=False)
    will = {}
    if will_exists:
        with st.expander("Will / Nomination details"):
            executor = st.text_input("Executor name")
            will_doc = st.file_uploader("Upload Will document (PDF) (optional)", type=["pdf"], key="will_doc")
            nominees = st.text_area("Nominees (one per line: name, relation, share%)")
            will = {"executor": executor, "nominees": [n.strip() for n in nominees.splitlines() if n.strip()]}

    st.markdown("---")
    st.subheader("Death / Closure (optional at creation time)")
    dod = st.date_input("Date of death (DOD) — fill only if applicable", value=None)
    death_doc = st.file_uploader("Death certificate (optional)", type=["pdf", "png", "jpg", "jpeg"], key="death_doc")

    submitted = st.form_submit_button("Preview & Save Submission")

# --- Preview and Save ---
if submitted:
    # Build a submission record
    record = {
        "created_at": datetime.utcnow().isoformat(),
        "full_name": full_name,
        "dob": str(dob) if dob else None,
        "dod": str(dod) if dod else None,
        "personal": {
            "gender": gender,
            "place_of_birth": place_of_birth,
        },
        "education": education_entries,
        "employment": employment_entries,
        "bank_accounts": bank_accounts,
        "investments": investments,
        "insurance": insurance_entries,
        "taxes": {
            "pan": st.session_state.get("tax_pan", ""),
            "tax_docs": [f.name for f in st.session_state.get("tax_docs", [])] if "tax_docs" in st.session_state else []
        },
        "will": will
    }

    # Save files
    birth_doc_path = save_uploaded_file(birth_doc, "birth")
    death_doc_path = save_uploaded_file(death_doc, "death")
    # Save tax docs
    saved_tax_paths = []
    if "tax_docs" in st.session_state:
        for f in st.session_state.get("tax_docs", []):
            p = save_uploaded_file(f, "tax")
            saved_tax_paths.append(p)

    # Add file paths into record for traceability
    record["birth_doc_path"] = birth_doc_path
    record["death_doc_path"] = death_doc_path
    record["tax_doc_paths"] = saved_tax_paths

    # Compute a deterministic proof snapshot and hash
    # Use the main structured fields + file names + timestamps
    snapshot = {
        "full_name": record["full_name"],
        "dob": record["dob"],
        "created_at": record["created_at"],
        "personal": record["personal"],
        "education": record["education"],
        "employment": record["employment"],
        "bank_accounts": record["bank_accounts"],
        "investments": record["investments"],
        "insurance": record["insurance"],
        "taxes": record["taxes"],
        "will": record["will"],
        "birth_doc": os.path.basename(birth_doc_path) if birth_doc_path else None,
        "death_doc": os.path.basename(death_doc_path) if death_doc_path else None,
        "tax_docs": [os.path.basename(x) for x in saved_tax_paths],
    }
    proof_hash = compute_proof_hash(snapshot)
    record["proof_hash"] = proof_hash

    # Show preview to user
    st.success("Preview generated — review the data below.")
    st.json(snapshot)
    st.markdown("**Submission Proof (SHA256)**")
    st.code(proof_hash)

    # Save record to DB (metadata only)
    save_submission(record)
    st.success("Submission saved locally (metadata to SQLite, files in ./uploads/).")

    # Downloads
    st.markdown("### Export / Downloads")
    export_json = json.dumps(snapshot, indent=2, sort_keys=True)
    st.download_button("Download submission JSON", export_json, file_name=f"submission_{record['full_name']}_{datetime.utcnow().strftime('%Y%m%d%H%M')}.json")

    # Guidance to publish proof on-chain or to IPFS
    st.markdown("### How to anchor this proof on-chain or to IPFS (manual steps)")
    st.write("""
    1. Copy the proof hash (above).  
    2. To pin on IPFS: create a small JSON with the hash and pin via a pinning service (or your node).  
    3. To store on-chain: use a wallet (MetaMask) and a small contract or an existing registry contract to store the hash (you must sign & pay gas from your wallet).  
    4. Optionally add the transaction hash / chain reference into the submission record (not automated here).
    """)

# --- Admin view / List stored submissions ---
st.markdown("---")
st.header("Admin: View saved submissions")
if st.checkbox("Show saved submissions and download CSV/JSON (admin)"):
    df = get_all_submissions_df()
    if df.empty:
        st.info("No submissions yet.")
    else:
        # Convert JSON columns for readable table
        disp = df[["id", "created_at", "full_name", "dob", "dod", "proof_hash"]].copy()
        st.dataframe(disp)
        # allow selecting a row to view details
        selected = st.number_input("Enter submission ID to view details", min_value=1, value=int(df.iloc[0]["id"]))
        row = df[df["id"] == int(selected)]
        if not row.empty:
            row = row.iloc[0].to_dict()
            st.subheader(f"Submission #{row['id']} — {row['full_name']}")
            # Pretty print each JSON field
            for key in ["personal", "education", "employment", "bank_accounts", "investments", "insurance", "taxes", "will"]:
                try:
                    st.markdown(f"**{key.title()}**")
                    st.json(json.loads(row.get(key) or "{}"))
                except Exception:
                    st.write(f"{key}: {row.get(key)}")
            st.write("Birth document path:", row.get("birth_doc_path"))
            st.write("Death document path:", row.get("death_doc_path"))
            st.write("Proof hash:", row.get("proof_hash"))
            # allow download of raw DB row as JSON
            st.download_button("Download row JSON", json.dumps(row, default=str, indent=2), file_name=f"submission_{row['id']}.json")

st.markdown("---")
st.caption("")
