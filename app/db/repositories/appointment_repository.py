from sqlalchemy.orm import Session

from app.db.models.appointment import Appointment


class AppointmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: dict) -> Appointment:
        appointment = Appointment(**data)
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def get_by_id(self, appointment_id: int) -> Appointment | None:
        return (
            self.db.query(Appointment)
            .filter(Appointment.id == appointment_id)
            .first()
        )

    def get_by_lead_id(self, lead_id: int) -> list[Appointment]:
        return (
            self.db.query(Appointment)
            .filter(Appointment.lead_id == lead_id)
            .order_by(Appointment.created_at.desc())
            .all()
        )

    def update(self, appointment: Appointment, data: dict) -> Appointment:
        for key, value in data.items():
            setattr(appointment, key, value)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment