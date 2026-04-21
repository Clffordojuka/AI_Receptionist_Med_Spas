from datetime import datetime, timedelta, timezone

from app.db.session import SessionLocal
from app.db.repositories.faq_repository import FAQRepository
from app.db.repositories.lead_repository import LeadRepository
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.followup_repository import FollowUpRepository


FAQS = [
    {
        "question": "What services do you offer?",
        "answer": "We offer Botox, fillers, facials, chemical peels, microneedling, consultations, and skin treatments.",
        "category": "services",
        "active": True,
    },
    {
        "question": "Where are you located?",
        "answer": "We are located at our med spa premises. Please contact us directly for full directions and landmark details.",
        "category": "location",
        "active": True,
    },
    {
        "question": "Do I need a consultation?",
        "answer": "Some treatments may require an initial consultation to confirm the best option for your needs.",
        "category": "consultation",
        "active": True,
    },
]

LEADS = [
    {
        "full_name": "Sarah Kim",
        "phone": "+254700123456",
        "email": "sarah@example.com",
        "source_channel": "webchat",
        "service_interest": "Botox",
        "new_or_returning": "new",
        "qualification_status": "in_progress",
        "booking_status": "pending",
        "lead_status": "qualifying",
        "handoff_requested": False,
    },
    {
        "full_name": "Brian Otieno",
        "phone": "+254711000111",
        "email": "brian@example.com",
        "source_channel": "whatsapp",
        "service_interest": "Facial",
        "new_or_returning": "returning",
        "qualification_status": "qualified",
        "booking_status": "confirmed",
        "lead_status": "booked",
        "handoff_requested": False,
    },
    {
        "full_name": "Diana Njeri",
        "phone": "+254722333444",
        "email": "diana@example.com",
        "source_channel": "sms",
        "service_interest": "Consultation",
        "new_or_returning": "new",
        "qualification_status": "in_progress",
        "booking_status": "pending",
        "lead_status": "pending_followup",
        "handoff_requested": True,
        "assigned_to": "Reception Team",
        "admin_notes": "Requested human callback.",
    },
]


def main():
    db = SessionLocal()
    faq_repo = FAQRepository(db)
    lead_repo = LeadRepository(db)
    convo_repo = ConversationRepository(db)
    followup_repo = FollowUpRepository(db)

    if not faq_repo.get_all_active():
        for item in FAQS:
            faq_repo.create(item)
        print("Seeded FAQs.")

    existing_leads = lead_repo.list_leads(limit=10)
    if not existing_leads:
        created = []
        for item in LEADS:
            created.append(lead_repo.create(item))
        print("Seeded demo leads.")

        convo_repo.create(
            lead_id=created[0].id,
            channel="webchat",
            message_role="user",
            message_text="Hi, I am interested in Botox and I am a new client.",
            intent="qualification",
            confidence_score=0.9,
        )
        convo_repo.create(
            lead_id=created[0].id,
            channel="webchat",
            message_role="assistant",
            message_text="I’d be glad to help. Could you share your preferred appointment day or time?",
            intent="qualification",
            confidence_score=0.9,
        )

        followup_repo.create(
            {
                "lead_id": created[2].id,
                "scheduled_for": datetime.now(timezone.utc) + timedelta(minutes=5),
                "status": "pending",
                "message_template": None,
                "attempt_number": 1,
            }
        )
        print("Seeded demo conversations and follow-up jobs.")
    else:
        print("Demo leads already exist. Skipping lead seed.")

    db.close()
    print("Demo seed complete.")


if __name__ == "__main__":
    main()