import json
import os
from typing import Any, Dict, Optional, Tuple

import requests
import streamlit as st


def get_base_url() -> str:
    if "base_url" not in st.session_state:
        default_host = os.getenv("BACKEND_HOST", "http://localhost")
        default_port = os.getenv("BACKEND_PORT", "4008")
        st.session_state.base_url = f"{default_host}:{default_port}"
    return st.session_state.base_url


def set_base_url(new_url: str) -> None:
    st.session_state.base_url = new_url.rstrip("/")


def call_api(
    method: str,
    path: str,
    json_body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, int, Any]:
    url = f"{get_base_url()}{path}"
    try:
        resp = requests.request(
            method=method.upper(),
            url=url,
            json=json_body,
            params=params,
            timeout=30,
        )
        content_type = resp.headers.get("content-type", "")
        if "application/json" in content_type:
            data = resp.json()
        else:
            data = resp.text
        return resp.ok, resp.status_code, data
    except requests.RequestException as e:
        return False, 0, str(e)


def show_response(ok: bool, status: int, data: Any) -> None:
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write("Status:")
        st.code(str(status))
    with col2:
        st.write("Response:")
        if isinstance(data, (dict, list)):
            st.json(data)
        else:
            st.code(str(data))
    if not ok:
        st.error("Request failed. See response for details.")


# -------------------------
# UI SECTIONS
# -------------------------

def vendor_registration_ui() -> None:
    st.subheader("Vendor Registration (/api/v1/vendore/vendeorReg)")
    with st.form("vendor_reg_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            org_name = st.text_input("Organization Name", placeholder="Acme Corp")
            reg_no = st.text_input("Registration No")
            org_type = st.text_input("Organization Type", placeholder="Private")
            name = st.text_input("Contact Person Name")
            contact = st.text_input("Contact Number")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
        with col_b:
            org_addr = st.text_input("Organization Address")
            city = st.text_input("City")
            state = st.text_input("State")
            country = st.text_input("Country")
            website = st.text_input("Website URL", placeholder="https://...")
            chain_csv = st.text_input("Chain Data (comma-separated)", placeholder="aptos")
        submitted = st.form_submit_button("Register Vendor")
    if submitted:
        chain_data = [s.strip() for s in chain_csv.split(",") if s.strip()] or []
        payload = {
            "chainData": chain_data,
            "password": password,
            "orgName": org_name,
            "regNo": reg_no,
            "orgType": org_type,
            "name": name,
            "contact": int(contact) if contact.isdigit() else contact,
            "email": email,
            "orgAddr": org_addr,
            "city": city,
            "state": state,
            "country": country,
            "websiteUrl": website,
        }
        ok, status, data = call_api("POST", "/api/v1/vendore/vendeorReg", json_body=payload)
        show_response(ok, status, data)


def vendor_login_ui() -> None:
    st.subheader("Vendor Login (/api/v1/vendore/VendeorLogin)")
    with st.form("vendor_login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted:
        payload = {"email": email, "password": password}
        ok, status, data = call_api("POST", "/api/v1/vendore/VendeorLogin", json_body=payload)
        show_response(ok, status, data)


def issue_document_ui() -> None:
    st.subheader("Issue Document (/api/v1/vendore/issue)")
    with st.form("issue_doc_form"):
        issuer = st.text_input("Issuer Identifier")
        receiver = st.text_input("Receiver Identifier")
        doc_type = st.text_input("Document Type", value="Birth_Certificate")
        doc_id = st.text_input("Document ID")
        metadata_text = st.text_area("Metadata (JSON)", value=json.dumps({"note": "example"}, indent=2))
        chain_csv = st.text_input("Chain (comma-separated)", placeholder="aptos")
        submitted = st.form_submit_button("Issue")
    if submitted:
        try:
            meta = json.loads(metadata_text) if metadata_text.strip() else {}
        except json.JSONDecodeError as e:
            st.error(f"Invalid metadata JSON: {e}")
            return
        chain = [s.strip() for s in chain_csv.split(",") if s.strip()]
        payload = {
            "issuer": issuer,
            "receiver": receiver,
            "docType": doc_type,
            "docId": doc_id,
            "metaData": meta,
            "chain": chain,
        }
        ok, status, data = call_api("POST", "/api/v1/vendore/issue", json_body=payload)
        show_response(ok, status, data)


def read_transaction_ui() -> None:
    st.subheader("Read Transaction (/api/v1/vendore/readData)")
    with st.form("read_tx_form"):
        trans_id = st.text_input("Transaction ID (hash)")
        method_choice = st.selectbox("HTTP Method", ["GET", "POST"], index=0)
        submitted = st.form_submit_button("Read")
    if submitted:
        payload = {"transId": trans_id}
        if method_choice == "GET":
            ok, status, data = call_api("GET", "/api/v1/vendore/readData", params=payload)
            if not ok or (isinstance(data, dict) and data.get("statusCode") in (400, 404)):
                ok, status, data = call_api("POST", "/api/v1/vendore/readData", json_body=payload)
        else:
            ok, status, data = call_api("POST", "/api/v1/vendore/readData", json_body=payload)
        show_response(ok, status, data)


def user_create_ui() -> None:
    st.subheader("Create User (/api/v1/user/createUser)")
    with st.form("user_create_form"):
        issuer = st.text_input("Issuer Identifier")
        col1, col2 = st.columns(2)
        with col1:
            baby_name = st.text_input("Baby Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            birth_date = st.date_input("Birth Date")
            time_of_birth = st.text_input("Time of Birth (HH:MM)")
            place_of_birth = st.text_input("Place of Birth")
            father_name = st.text_input("Father Name")
            father_id = st.text_input("Father ID")
            father_contact = st.text_input("Father Contact")
            father_email = st.text_input("Father Email")
        with col2:
            mother_name = st.text_input("Mother Name")
            mother_id = st.text_input("Mother ID")
            mother_contact = st.text_input("Mother Contact")
            mother_email = st.text_input("Mother Email")
            address = st.text_input("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            country = st.text_input("Country")
        submitted = st.form_submit_button("Create User Record")
    if submitted:
        payload = {
            "issuer": issuer,
            "babyName": baby_name,
            "gender": gender,
            "birthDate": birth_date.isoformat(),
            "timeOfBirth": time_of_birth,
            "placeOfBirth": place_of_birth,
            "fatherName": father_name,
            "fatherId": father_id,
            "fatherContact": father_contact,
            "fatherEmail": father_email,
            "motherName": mother_name,
            "motherId": mother_id,
            "motherContact": mother_contact,
            "motherEmail": mother_email,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
        }
        ok, status, data = call_api("POST", "/api/v1/user/createUser", json_body=payload)
        show_response(ok, status, data)


def user_login_ui() -> None:
    st.subheader("User Login (/api/v1/user/loginUser)")
    with st.form("user_login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted:
        payload = {"email": email, "password": password}
        ok, status, data = call_api("POST", "/api/v1/user/loginUser", json_body=payload)
        show_response(ok, status, data)


# NEW: History UI (multi tx retrieval)
def transaction_history_ui() -> None:
    st.subheader("Transaction History (bulk read)")
    st.caption("Enter one or more transaction IDs separated by commas")
    with st.form("bulk_history_form"):
        trans_ids = st.text_area("Transaction IDs", placeholder="tx1, tx2, tx3")
        submitted = st.form_submit_button("Fetch History")
    if submitted:
        ids = [t.strip() for t in trans_ids.split(",") if t.strip()]
        results = []
        for t in ids:
            ok, status, data = call_api("POST", "/api/v1/vendore/readData", json_body={"transId": t})
            results.append({"id": t, "status": status, "data": data})
        st.write("### Results")
        for r in results:
            st.markdown(f"**Transaction {r['id']}** (status {r['status']})")
            if isinstance(r["data"], (dict, list)):
                st.json(r["data"])
            else:
                st.code(str(r["data"]))
            st.divider()


def main() -> None:
    st.set_page_config(page_title="Aptos CivicChain Frontend", page_icon="🧾", layout="wide")
    st.title("CivicChain API Frontend")

    with st.sidebar:
        st.header("Configuration")
        base_url = st.text_input("Backend Base URL", value=get_base_url())
        if base_url:
            set_base_url(base_url)
        st.caption("Default is http://localhost:4008.")

        side = st.radio("Section", [
            "Vendor Registration",
            "Vendor Login",
            "Issue Document",
            "Read Transaction",
            "Transaction History",
            "Create User",
            "User Login",
        ])

    if side == "Vendor Registration":
        vendor_registration_ui()
    elif side == "Vendor Login":
        vendor_login_ui()
    elif side == "Issue Document":
        issue_document_ui()
    elif side == "Read Transaction":
        read_transaction_ui()
    elif side == "Transaction History":
        transaction_history_ui()
    elif side == "Create User":
        user_create_ui()
    elif side == "User Login":
        user_login_ui()


if __name__ == "__main__":
    main()
