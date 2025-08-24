import json
import os
from typing import Any, Dict, Optional, Tuple

import requests
import streamlit as st

# Simple theming tweaks
st.markdown(
	"""
	<style>
		.small-muted { color: #777; font-size: 0.9rem; }
		.header-pill {
			padding: 0.35rem 0.75rem; border-radius: 999px; background: #eef6ff; color: #1e5fb3; display: inline-block;
		}
	</style>
	""",
	unsafe_allow_html=True,
)

# Session helpers

def init_session() -> None:
	if "authenticated" not in st.session_state:
		st.session_state.authenticated = False
	if "auth_role" not in st.session_state:
		st.session_state.auth_role = None  # 'vendor' or 'user'
	if "auth_email" not in st.session_state:
		st.session_state.auth_email = ""
	if "auth_profile" not in st.session_state:
		st.session_state.auth_profile = None


def set_auth(role: str, email: str, profile: Any) -> None:
	st.session_state.authenticated = True
	st.session_state.auth_role = role
	st.session_state.auth_email = email
	st.session_state.auth_profile = profile


def sign_out() -> None:
	st.session_state.authenticated = False
	st.session_state.auth_role = None
	st.session_state.auth_email = ""
	st.session_state.auth_profile = None


def get_base_url() -> str:
	if "base_url" not in st.session_state:
		default_host = os.getenv("BACKEND_HOST", "http://localhost")
		default_port = os.getenv("BACKEND_PORT", "4008")
		st.session_state.base_url = f"{default_host}:{default_port}"
	return st.session_state.base_url


def set_base_url(new_url: str) -> None:
	st.session_state.base_url = new_url.rstrip("/")


def call_api(method: str, path: str, json_body: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Tuple[bool, int, Any]:
	url = f"{get_base_url()}{path}"
	try:
		resp = requests.request(method=method.upper(), url=url, json=json_body, params=params, timeout=30)
		content_type = resp.headers.get("content-type", "")
		data: Any
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
		if ok and status == 200:
			profile = data.get("data") if isinstance(data, dict) else None
			set_auth("vendor", email, profile)
			st.success("Registered and logged in as vendor")
			try:
				st.rerun()
			except Exception:
				pass


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
		if ok and status == 200:
			profile = data.get("data") if isinstance(data, dict) else None
			set_auth("vendor", email, profile)
			st.success("Logged in as vendor")
			try:
				st.rerun()
			except Exception:
				pass


def issue_document_ui() -> None:
	st.subheader("Issue Document (/api/v1/vendore/issue)")
	st.caption("Issuer and Receiver should correspond to records that exist in the backend database so their wallet IDs can be resolved.")
	with st.form("issue_doc_form"):
		issuer = st.text_input("Issuer Identifier (e.g., vendor email or unique ID)")
		receiver = st.text_input("Receiver Identifier (e.g., user email or unique ID)")
		doc_type = st.text_input("Document Type", value="Birth_Certificate")
		doc_id = st.text_input("Document ID")
		metadata_text = st.text_area("Metadata (JSON)", value=json.dumps({"note": "example"}, indent=2))
		chain_csv = st.text_input("Chain (comma-separated)", placeholder="aptos")
		submitted = st.form_submit_button("Issue")
	if submitted:
		try:
			meta: Any = json.loads(metadata_text) if metadata_text.strip() else {}
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
		method_choice = st.selectbox("HTTP Method (backend expects GET but reads body)", ["GET", "POST"], index=0)
		submitted = st.form_submit_button("Read")
	if submitted:
		payload = {"transId": trans_id}
		if method_choice == "GET":
			# Backend reads from req.body even on GET; attempt as query param
			ok, status, data = call_api("GET", "/api/v1/vendore/readData", params=payload)
			# If it fails, try POST as a fallback due to backend mismatch
			if not ok or (isinstance(data, dict) and data.get("statusCode") in (400, 404)):
				ok, status, data = call_api("POST", "/api/v1/vendore/readData", json_body=payload)
		else:
			ok, status, data = call_api("POST", "/api/v1/vendore/readData", json_body=payload)
		show_response(ok, status, data)


def user_create_ui() -> None:
	st.subheader("Create User (/api/v1/user/createUser)")
	st.caption("This will also create a wallet and store a document on-chain. 'issuer' should reference the issuing authority.")
	with st.form("user_create_form"):
		issuer = st.text_input("Issuer Identifier (e.g., vendor email or unique ID)")
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
		ok, status, data = call_api("PATCH", "/api/v1/user/createUser", json_body=payload)
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
		if ok and status == 200:
			profile = data.get("data") if isinstance(data, dict) else None
			set_auth("user", email, profile)
			st.success("Logged in as user")
			try:
				st.rerun()
			except Exception:
				pass


def main() -> None:
	st.set_page_config(page_title="Aptos CivicChain Frontend", page_icon="🧾", layout="wide")
	init_session()
	st.title("CivicChain API Frontend")
	st.write("Interact with the Express backend APIs from a Streamlit UI.")

	with st.sidebar:
		st.header("Configuration")
		base_url = st.text_input("Backend Base URL", value=get_base_url())
		if base_url:
			set_base_url(base_url)
		st.caption("Default is http://localhost:4008. Change if backend runs elsewhere.")
		st.divider()
		if st.session_state.authenticated:
			st.markdown(f"**Signed in:** {st.session_state.auth_role} · {st.session_state.auth_email}")
			if st.button("Sign out"):
				sign_out()
				st.success("Signed out")
				try:
					st.rerun()
				except Exception:
					pass

	if not st.session_state.authenticated:
		st.markdown('<span class="header-pill">Authentication Required</span>', unsafe_allow_html=True)
		st.write("Please login or register to continue.")
		role = st.radio("I am a", ["Vendor", "User"], horizontal=True)
		action = st.radio("Action", ["Login", "Register"], horizontal=True)
		if role == "Vendor":
			if action == "Login":
				vendor_login_ui()
			else:
				vendor_registration_ui()
		else:
			if action == "Login":
				user_login_ui()
			else:
				user_create_ui()
	else:
		st.markdown('<span class="header-pill">Authenticated</span>', unsafe_allow_html=True)
		st.write(f"Welcome, {st.session_state.auth_email} ({st.session_state.auth_role}).")
		if st.session_state.auth_role == "vendor":
			vendor_tabs = st.tabs(["Issue Document", "Read Transaction", "Create User"])
			with vendor_tabs[0]:
				issue_document_ui()
			with vendor_tabs[1]:
				read_transaction_ui()
			with vendor_tabs[2]:
				user_create_ui()
		else:
			user_tabs = st.tabs(["Read Transaction"]) 
			with user_tabs[0]:
				read_transaction_ui()

	st.divider()
	st.caption("Note: Some backend routes appear to have inconsistencies (e.g., GET reading request body, missing leading '/' in user mount). This UI attempts sensible fallbacks, but backend fixes may be required.")


if __name__ == "__main__":
	main()