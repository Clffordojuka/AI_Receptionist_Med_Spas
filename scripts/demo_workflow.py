import requests

BASE_URL = "http://127.0.0.1:8000"


def main():
    lead_payload = {
        "full_name": "Demo User",
        "phone": "+254708081885",
        "email": "demo@example.com",
        "source_channel": "webchat",
        "service_interest": "Microneedling",
        "new_or_returning": "new",
    }

    lead = requests.post(f"{BASE_URL}/api/leads", json=lead_payload, timeout=30).json()
    lead_id = lead["id"]
    print("Created lead:", lead_id)

    chat_payload = {
        "lead_id": lead_id,
        "message": "Hi, I am interested in microneedling and I am a new client.",
        "channel": "webchat",
    }
    chat_result = requests.post(f"{BASE_URL}/api/chat/message", json=chat_payload, timeout=60).json()
    print("Chat result:", chat_result)

    slots = requests.get(
        f"{BASE_URL}/api/bookings/slots",
        params={"lead_id": lead_id, "service_name": "Microneedling"},
        timeout=30,
    ).json()
    print("Slots:", slots[:2])

    if slots:
        booking_payload = {
            "lead_id": lead_id,
            "service_name": "Microneedling",
            "appointment_datetime": slots[0]["start_time"],
            "provider_name": slots[0]["provider_name"],
            "notes": "Demo booking flow",
        }
        booking = requests.post(f"{BASE_URL}/api/bookings/create", json=booking_payload, timeout=30).json()
        print("Booking:", booking)

    review = requests.get(f"{BASE_URL}/api/admin/leads/{lead_id}/review", timeout=30).json()
    print("Lead review:", review)


if __name__ == "__main__":
    main()