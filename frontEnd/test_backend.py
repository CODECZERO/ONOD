import os
import sys
import time
import uuid
import json
from typing import Any, Dict, Optional, Tuple

import requests


def build_base_url() -> str:
	default_host = os.getenv("BACKEND_HOST", "http://localhost")
	default_port = os.getenv("BACKEND_PORT", "4008")
	return f"{default_host}:{default_port}"


class ApiTester:
	def __init__(self, base_url: str) -> None:
		self.base_url = base_url.rstrip("/")
		self.results: Dict[str, Dict[str, Any]] = {}
		self.vendor1: Dict[str, Any] = {}
		self.vendor2: Dict[str, Any] = {}
		self.last_tx_id: Optional[str] = None

	def _request(self, method: str, path: str, json_body: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Tuple[bool, int, Any]:
		url = f"{self.base_url}{path}"
		try:
			resp = requests.request(method=method.upper(), url=url, json=json_body, params=params, timeout=30)
			content_type = resp.headers.get("content-type", "")
			data = resp.json() if "application/json" in content_type else resp.text
			return resp.ok, resp.status_code, data
		except requests.RequestException as e:
			return False, 0, str(e)

	def _record(self, name: str, ok: bool, status: int, data: Any) -> None:
		self.results[name] = {
			"ok": ok,
			"status": status,
			"data": data,
		}

	def register_vendor(self, label: str) -> Tuple[str, str]:
		# Generate unique email and simple password
		uniq = uuid.uuid4().hex[:8]
		email = f"{label.lower()}_{uniq}@example.com"
		password = "TestPass!123"
		payload = {
			"chainData": ["aptos"],
			"password": password,
			"orgName": f"{label} Org",
			"regNo": f"REG-{uniq}",
			"orgType": "Private",
			"name": f"{label} Admin",
			"contact": "1234567890",
			"email": email,
			"orgAddr": "123 Test St",
			"city": "Testville",
			"state": "TS",
			"country": "Nowhere",
			"websiteUrl": "https://example.com",
		}
		ok, status, data = self._request("POST", "/api/v1/vendore/vendeorReg", json_body=payload)
		self._record(f"{label}_register_vendor", ok, status, data)
		return email, password

	def login_vendor(self, email: str, password: str, label: str) -> None:
		payload = {"email": email, "password": password}
		ok, status, data = self._request("POST", "/api/v1/vendore/VendeorLogin", json_body=payload)
		self._record(f"{label}_login_vendor", ok, status, data)

	def issue_document(self, issuer_identifier: str, receiver_identifier: str) -> None:
		payload = {
			"issuer": issuer_identifier,
			"receiver": receiver_identifier,
			"docType": "TestDoc",
			"docId": f"DOC-{uuid.uuid4().hex[:10]}",
			"metaData": {"note": "backend test"},
			"chain": ["aptos"],
		}
		ok, status, data = self._request("POST", "/api/v1/vendore/issue", json_body=payload)
		self._record("issue_document", ok, status, data)
		# Try to extract a transaction id
		if ok:
			# Common shapes: {statusCode, data: {transId: [...]}} or {statusCode, data: "0xabc..."}
			if isinstance(data, dict):
				inner = data.get("data")
				if isinstance(inner, dict):
					# pick last transId if available
					trans_list = inner.get("transId") if isinstance(inner.get("transId"), list) else None
					if trans_list:
						self.last_tx_id = trans_list[-1]
				elif isinstance(inner, str):
					self.last_tx_id = inner

	def read_transaction(self) -> None:
		if not self.last_tx_id:
			self._record("read_transaction", False, 0, "No transaction id available from issue step")
			return
		payload = {"transId": self.last_tx_id}
		# Try GET first with params, then POST fallback
		ok, status, data = self._request("GET", "/api/v1/vendore/readData", params=payload)
		if not ok or (isinstance(data, dict) and data.get("statusCode") in (400, 404)):
			ok, status, data = self._request("POST", "/api/v1/vendore/readData", json_body=payload)
		self._record("read_transaction", ok, status, data)

	def create_user(self, issuer_identifier: str) -> None:
		# Build a minimal valid user record
		uniq = uuid.uuid4().hex[:8]
		payload = {
			"issuer": issuer_identifier,
			"babyName": f"Baby-{uniq}",
			"gender": "Other",
			"birthDate": time.strftime("%Y-%m-%d"),
			"timeOfBirth": "12:00",
			"placeOfBirth": "Test Hospital",
			"fatherName": "Test Father",
			"fatherId": f"FID-{uniq}",
			"fatherContact": "1234567890",
			"fatherEmail": f"father_{uniq}@example.com",
			"motherName": "Test Mother",
			"motherId": f"MID-{uniq}",
			"motherContact": "0987654321",
			"motherEmail": f"mother_{uniq}@example.com",
			"address": "456 Family Rd",
			"city": "Testcity",
			"state": "TS",
			"country": "Nowhere",
		}
		ok, status, data = self._request("PATCH", "/api/v1/user/createUser", json_body=payload)
		# If route is not mounted due to missing slash in server, report clearly
		if not ok and status == 404:
			self._record("create_user", ok, status, {"hint": "User router may not be mounted (missing leading '/' in app.use)."})
		else:
			self._record("create_user", ok, status, data)

	def login_user(self, email: str, password: str) -> None:
		payload = {"email": email, "password": password}
		ok, status, data = self._request("POST", "/api/v1/user/loginUser", json_body=payload)
		self._record("login_user", ok, status, data)

	def run(self) -> int:
		# Register two vendors (issuer and receiver)
		v1_email, v1_pass = self.register_vendor("VendorA")
		self.vendor1 = {"email": v1_email, "password": v1_pass}
		v2_email, v2_pass = self.register_vendor("VendorB")
		self.vendor2 = {"email": v2_email, "password": v2_pass}

		# Login first vendor
		self.login_vendor(v1_email, v1_pass, "VendorA")

		# Issue a test document from vendor A to vendor B
		self.issue_document(issuer_identifier=v1_email, receiver_identifier=v2_email)

		# Read the transaction if available
		self.read_transaction()

		# Create a user (issuer is vendor A)
		self.create_user(issuer_identifier=v1_email)

		# Attempt a user login with fatherEmail (likely to fail given backend logic)
		father_email = None
		create_user_data = self.results.get("create_user", {}).get("data")
		if isinstance(create_user_data, dict):
			inner = create_user_data.get("data") if isinstance(create_user_data.get("data"), dict) else create_user_data
			if isinstance(inner, dict):
				father_email = inner.get("fatherEmail")
		if father_email:
			self.login_user(email=father_email, password="wrong-password")
		else:
			self._record("login_user", False, 0, "Skipped (no fatherEmail returned from create_user)")

		# Print summary
		print("\n===== Backend API Test Summary =====")
		failures = 0
		for name, res in self.results.items():
			status = res.get("status")
			ok = res.get("ok")
			flag = "PASS" if ok and (isinstance(status, int) and 200 <= status < 300) else "FAIL"
			if flag == "FAIL":
				failures += 1
			print(f"- {name}: {flag} (HTTP {status})")
			if flag == "FAIL":
				print(f"  Details: {json.dumps(res.get('data'), default=str)[:500]}")
		print("===================================\n")

		return 0 if failures == 0 else 1


def main() -> None:
	base_url = os.getenv("BACKEND_BASE_URL") or (sys.argv[1] if len(sys.argv) > 1 else build_base_url())
	print(f"Using backend: {base_url}")
	tester = ApiTester(base_url)
	exit_code = tester.run()
	sys.exit(exit_code)


if __name__ == "__main__":
	main()