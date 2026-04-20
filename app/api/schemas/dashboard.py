from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_leads: int
    booked_leads: int
    handoff_leads: int
    pending_followup_leads: int
    qualifying_leads: int