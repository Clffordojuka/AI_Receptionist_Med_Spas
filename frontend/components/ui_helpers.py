import pandas as pd


def short_name(full_name: str | None) -> str:
    if not full_name:
        return "Unknown Lead"
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0]
    return f"{parts[0]} {parts[1][0]}."


def mask_phone(phone: str | None) -> str:
    if not phone:
        return "Not available"
    phone = str(phone)
    if len(phone) < 7:
        return phone
    return f"{phone[:5]}•••{phone[-3:]}"


def mask_email(email: str | None) -> str:
    if not email or "@" not in email:
        return "Not available"
    name, domain = email.split("@", 1)
    if len(name) <= 2:
        masked_name = name[0] + "•"
    else:
        masked_name = name[:2] + "•••"
    return f"{masked_name}@{domain}"


def display_status(value: str | None) -> str:
    if not value:
        return "Not set"
    return value.replace("_", " ").title()


def prepare_lead_inbox_dataframe(leads: list[dict]) -> pd.DataFrame:
    rows = []
    for lead in leads:
        rows.append(
            {
                "Lead ID": lead.get("id"),
                "Lead": short_name(lead.get("full_name")),
                "Phone": mask_phone(lead.get("phone")),
                "Email": mask_email(lead.get("email")),
                "Service": lead.get("service_interest") or "Not specified",
                "Lead Stage": display_status(lead.get("lead_status")),
                "Booking": display_status(lead.get("booking_status")),
                "Qualification": display_status(lead.get("qualification_status")),
                "Assigned To": lead.get("assigned_to") or "Unassigned",
                "Handoff": "Yes" if lead.get("handoff_requested") else "No",
                "Updated At": lead.get("updated_at"),
            }
        )
    return pd.DataFrame(rows)