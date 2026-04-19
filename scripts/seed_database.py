from app.db.session import SessionLocal
from app.db.repositories.faq_repository import FAQRepository


SEED_FAQS = [
    {
        "question": "What services do you offer?",
        "answer": "We offer services such as Botox, fillers, facials, chemical peels, microneedling, and consultations.",
        "category": "services",
        "active": True,
    },
    {
        "question": "Where are you located?",
        "answer": "We are conveniently located at our med spa location. Please contact us directly for the exact address and directions.",
        "category": "location",
        "active": True,
    },
    {
        "question": "What are your opening hours?",
        "answer": "Our operating hours vary by day, but we generally serve clients during regular business hours. Please ask for the latest availability when booking.",
        "category": "hours",
        "active": True,
    },
    {
        "question": "Do I need a consultation before treatment?",
        "answer": "Yes, some treatments may require an initial consultation to understand your needs and confirm the best option for you.",
        "category": "consultation",
        "active": True,
    },
    {
        "question": "How do I book an appointment?",
        "answer": "You can book an appointment by telling us the service you want and your preferred date or time, and we will guide you through the scheduling process.",
        "category": "booking",
        "active": True,
    },
]


def main():
    db = SessionLocal()
    repo = FAQRepository(db)

    existing = repo.get_all_active()
    if existing:
        print("FAQs already exist. Skipping seed.")
        db.close()
        return

    for item in SEED_FAQS:
        repo.create(item)

    print("FAQ seed completed successfully.")
    db.close()


if __name__ == "__main__":
    main()