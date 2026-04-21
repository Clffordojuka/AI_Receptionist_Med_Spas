import requests


class APIClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def _handle_response(self, response: requests.Response):
        try:
            data = response.json()
        except ValueError:
            data = None

        if not response.ok:
            if isinstance(data, dict):
                detail = data.get("detail") or data.get("message") or str(data)
            else:
                detail = response.text or f"HTTP {response.status_code}"
            raise Exception(f"API Error ({response.status_code}): {detail}")

        return data

    def _get(self, path: str, params: dict | None = None, timeout: int = 30):
        response = requests.get(f"{self.base_url}{path}", params=params, timeout=timeout)
        return self._handle_response(response)

    def _post(self, path: str, payload: dict | None = None, timeout: int = 30):
        response = requests.post(f"{self.base_url}{path}", json=payload, timeout=timeout)
        return self._handle_response(response)

    def _patch(self, path: str, payload: dict | None = None, timeout: int = 30):
        response = requests.patch(f"{self.base_url}{path}", json=payload, timeout=timeout)
        return self._handle_response(response)

    def health(self):
        return self._get("/api/health", timeout=20)

    def create_lead(self, payload: dict):
        return self._post("/api/leads", payload, timeout=30)

    def list_leads(
        self,
        lead_status: str | None = None,
        booking_status: str | None = None,
        qualification_status: str | None = None,
        handoff_requested: bool | None = None,
        limit: int = 100,
    ):
        params = {"limit": limit}
        if lead_status:
            params["lead_status"] = lead_status
        if booking_status:
            params["booking_status"] = booking_status
        if qualification_status:
            params["qualification_status"] = qualification_status
        if handoff_requested is not None:
            params["handoff_requested"] = handoff_requested
        return self._get("/api/leads", params=params, timeout=30)

    def get_lead(self, lead_id: int):
        return self._get(f"/api/leads/{lead_id}", timeout=20)

    def update_lead(self, lead_id: int, payload: dict):
        return self._patch(f"/api/leads/{lead_id}", payload, timeout=30)

    def send_chat_message(self, payload: dict):
        return self._post("/api/chat/message", payload, timeout=60)

    def get_chat_history(self, lead_id: int):
        return self._get(f"/api/chat/history/{lead_id}", timeout=30)

    def get_slots(self, lead_id: int, service_name: str | None = None, date: str | None = None):
        params = {"lead_id": lead_id}
        if service_name:
            params["service_name"] = service_name
        if date:
            params["date"] = date
        return self._get("/api/bookings/slots", params=params, timeout=30)

    def create_booking(self, payload: dict):
        return self._post("/api/bookings/create", payload, timeout=30)

    def get_lead_bookings(self, lead_id: int):
        return self._get(f"/api/bookings/lead/{lead_id}", timeout=20)

    def create_followup(self, payload: dict):
        return self._post("/api/followups", payload, timeout=30)

    def auto_schedule_followup(self, lead_id: int):
        return self._post(f"/api/followups/auto/{lead_id}", timeout=30)

    def run_followups(self):
        return self._post("/api/followups/run", timeout=60)

    def get_lead_followups(self, lead_id: int):
        return self._get(f"/api/followups/lead/{lead_id}", timeout=20)

    def update_admin_fields(self, lead_id: int, payload: dict):
        return self._patch(f"/api/admin/leads/{lead_id}", payload, timeout=30)

    def escalate_lead(self, lead_id: int, payload: dict):
        return self._post(f"/api/admin/leads/{lead_id}/escalate", payload, timeout=30)

    def get_lead_review(self, lead_id: int):
        return self._get(f"/api/admin/leads/{lead_id}/review", timeout=30)

    def get_dashboard_summary(self):
        return self._get("/api/dashboard/summary", timeout=20)