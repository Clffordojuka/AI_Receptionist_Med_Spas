"""initial schema

Revision ID: 32514040769b
Revises: 
Create Date: 2026-04-22 01:12:45.689947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32514040769b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "faqs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("question", sa.String(length=500), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index(op.f("ix_faqs_id"), "faqs", ["id"], unique=False)

    op.create_table(
        "leads",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("source_channel", sa.String(length=100), nullable=False, server_default="webchat"),
        sa.Column("service_interest", sa.String(length=255), nullable=True),
        sa.Column("new_or_returning", sa.String(length=50), nullable=True),
        sa.Column("qualification_status", sa.String(length=50), nullable=False, server_default="unknown"),
        sa.Column("booking_status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("lead_status", sa.String(length=50), nullable=False, server_default="new"),
        sa.Column("assigned_to", sa.String(length=255), nullable=True),
        sa.Column("admin_notes", sa.Text(), nullable=True),
        sa.Column("handoff_requested", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("last_contacted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index(op.f("ix_leads_id"), "leads", ["id"], unique=False)

    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("service_name", sa.String(length=255), nullable=True),
        sa.Column("appointment_datetime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("provider_name", sa.String(length=255), nullable=True),
        sa.Column("calendar_event_id", sa.String(length=255), nullable=True),
        sa.Column("booking_status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"]),
    )
    op.create_index(op.f("ix_appointments_id"), "appointments", ["id"], unique=False)
    op.create_index(op.f("ix_appointments_lead_id"), "appointments", ["lead_id"], unique=False)

    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=100), nullable=False, server_default="webchat"),
        sa.Column("message_role", sa.String(length=50), nullable=False),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column("intent", sa.String(length=100), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"]),
    )
    op.create_index(op.f("ix_conversations_id"), "conversations", ["id"], unique=False)
    op.create_index(op.f("ix_conversations_lead_id"), "conversations", ["lead_id"], unique=False)

    op.create_table(
        "followup_jobs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("message_template", sa.Text(), nullable=True),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"]),
    )
    op.create_index(op.f("ix_followup_jobs_id"), "followup_jobs", ["id"], unique=False)
    op.create_index(op.f("ix_followup_jobs_lead_id"), "followup_jobs", ["lead_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f("ix_followup_jobs_lead_id"), table_name="followup_jobs")
    op.drop_index(op.f("ix_followup_jobs_id"), table_name="followup_jobs")
    op.drop_table("followup_jobs")

    op.drop_index(op.f("ix_conversations_lead_id"), table_name="conversations")
    op.drop_index(op.f("ix_conversations_id"), table_name="conversations")
    op.drop_table("conversations")

    op.drop_index(op.f("ix_appointments_lead_id"), table_name="appointments")
    op.drop_index(op.f("ix_appointments_id"), table_name="appointments")
    op.drop_table("appointments")

    op.drop_index(op.f("ix_leads_id"), table_name="leads")
    op.drop_table("leads")

    op.drop_index(op.f("ix_faqs_id"), table_name="faqs")
    op.drop_table("faqs")