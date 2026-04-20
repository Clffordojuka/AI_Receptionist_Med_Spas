import requests


class APIClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def _handle_response(self, response: requests.Response):
        try:
            data = response.json()
        except Exception:
            response.raise_for_status()
            return None

        if not response.ok:
            detail = data.get("detail", response.text) if isinstance(data, dict) else response.text
            raise Exception(f"API Error: {detail}")

        return data

    def health(self):
        response = requests.get(f"{self.base_url}/api/health", timeout=20)
        return self._handle_response(response)

    def create_lead(self, payload: dict):
        response = requests.post(f"{self.base_url}/api/leads", json=payload, timeout=30)
        return self._handle_response(response)

    def get_lead(self, lead_id: int):
        response = requests.get(f"{self.base_url}/api/leads/{lead_id}", timeout=20)
        return self._handle_response(response)

    def update_lead(self, lead_id: int, payload: dict):
        response = requests.patch(f"{self.base_url}/api/leads/{lead_id}", json=payload, timeout=30)
        return self._handle_response(response)

    def send_chat_message(self, payload: dict):
        response = requests.post(f"{self.base_url}/api/chat/message", json=payload, timeout=60)
        return self._handle_response(response)

    def get_chat_history(self, lead_id: int):
        response = requests.get(f"{self.base_url}/api/chat/history/{lead_id}", timeout=30)
        return self._handle_response(response)

    def get_slots(self, lead_id: int, service_name: str | None = None, date: str | None = None):
        params = {"lead_id": lead_id}
        if service_name:
            params["service_name"] = service_name
        if date:
            params["date"] = date

        response = requests.get(f"{self.base_url}/api/bookings/slots", params=params, timeout=30)
        return self._handle_response(response)

    def create_booking(self, payload: dict):
        response = requests.post(f"{self.base_url}/api/bookings/create", json=payload, timeout=30)
        return self._handle_response(response)

    def get_lead_bookings(self, lead_id: int):
        response = requests.get(f"{self.base_url}/api/bookings/lead/{lead_id}", timeout=20)
        return self._handle_response(response)

    def create_followup(self, payload: dict):
        response = requests.post(f"{self.base_url}/api/followups", json=payload, timeout=30)
        return self._handle_response(response)

    def auto_schedule_followup(self, lead_id: int):
        response = requests.post(f"{self.base_url}/api/followups/auto/{lead_id}", timeout=30)
        return self._handle_response(response)

    def run_followups(self):
        response = requests.post(f"{self.base_url}/api/followups/run", timeout=60)
        return self._handle_response(response)

    def get_lead_followups(self, lead_id: int):
        response = requests.get(f"{self.base_url}/api/followups/lead/{lead_id}", timeout=20)
        return self._handle_response(response)

    def update_admin_fields(self, lead_id: int, payload: dict):
        response = requests.patch(f"{self.base_url}/api/admin/leads/{lead_id}", json=payload, timeout=30)
        return self._handle_response(response)

    def escalate_lead(self, lead_id: int, payload: dict):
        response = requests.post(f"{self.base_url}/api/admin/leads/{lead_id}/escalate", json=payload, timeout=30)
        return self._handle_response(response)

    def get_lead_review(self, lead_id: int):
        response = requests.get(f"{self.base_url}/api/admin/leads/{lead_id}/review", timeout=30)
        return self._handle_response(response)
    
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

        response = requests.get(f"{self.base_url}/api/leads", params=params, timeout=30)
        return self._handle_response(response)

    def get_dashboard_summary(self):
        response = requests.get(f"{self.base_url}/api/dashboard/summary", timeout=20)
        return self._handle_response(response)