# AI Receptionist for Med Spas

## Purpose

This document defines the implementation skill guide for building an **AI Receptionist for Med Spas** as a personal project. It is intended to guide development from planning to deployment.

The system should be able to:

- capture incoming leads
- respond instantly through chat or messaging
- qualify leads
- answer common service questions
- book appointments through calendar integration
- follow up automatically when a lead does not book
- store conversations and lead outcomes for review

This project should be built like a real production-ready automation system, even if the first version is an MVP.

---

# 1. Product Vision

The AI Receptionist acts like a virtual front-desk assistant for med spas. It should handle repetitive lead communication automatically while maintaining a professional, friendly, and conversion-focused interaction style.

The system must support these business outcomes:

- reduce missed leads
- improve response speed
- automate appointment booking
- reduce manual receptionist workload
- improve conversion from inquiry to appointment

---

# 2. Core System Capabilities

## 2.1 Lead Intake
The system must accept new leads from one or more channels:

- website chatbot
- SMS
- WhatsApp
- Instagram/Facebook DM proxy workflows
- voice intake (future phase)

## 2.2 Instant Response
The assistant should immediately greet the lead, understand intent, and continue the conversation naturally.

## 2.3 Lead Qualification
The assistant should collect relevant information such as:

- full name
- phone number
- email
- service of interest
- preferred appointment date/time
- new or returning client status
- urgent questions or objections

## 2.4 FAQ Handling
The assistant should answer common questions about:

- available services
- location
- business hours
- pricing guidance
- booking policy
- consultation process

## 2.5 Appointment Booking
The assistant should:

- fetch available slots
- present options
- confirm selected slot
- create appointment
- send confirmation

## 2.6 Follow-Up Automation
If the lead does not book, the system should:

- mark the lead as pending
- schedule follow-up messages
- re-engage after a defined delay
- stop follow-up after booking or manual closure

## 2.7 Human Handoff
The system should support escalation when:

- lead asks complex questions
- lead requests a real human
- bot confidence is low
- booking flow fails
- complaint/sensitive issue is detected

---

# 3. Recommended Development Phases

## Phase 1 — MVP Chat Receptionist
Build the first working version with:

- web chat interface
- AI conversation engine
- lead capture
- FAQ answering
- conversation logging

## Phase 2 — Qualification + Booking
Add:

- qualification workflow
- calendar integration
- slot checking
- appointment confirmation

## Phase 3 — Follow-Up Automation
Add:

- follow-up scheduler
- reminder workflows
- re-engagement logic
- lead state transitions

## Phase 4 — Multi-Channel Support
Add:

- SMS integration
- WhatsApp integration
- webhook routing for external channels

## Phase 5 — Voice Receptionist
Add:

- Twilio voice or similar telephony layer
- speech-to-text and text-to-speech pipeline
- call flow orchestration

---

# 4. Project Architecture

The system should be organized into modular layers.

## 4.1 Presentation Layer
Handles user-facing interaction channels.

Examples:

- chat widget
- SMS endpoint
- WhatsApp webhook
- admin dashboard

## 4.2 Application Layer
Implements workflows and orchestration.

Examples:

- lead qualification logic
- booking flow
- follow-up scheduler
- handoff logic

## 4.3 AI Layer
Handles conversation intelligence.

Examples:

- prompt templates
- intent detection
- FAQ retrieval
- response generation
- confidence routing

## 4.4 Integration Layer
Connects external services.

Examples:

- calendar API
- Twilio
- email/SMS notification services
- CRM or database hooks

## 4.5 Data Layer
Stores business and conversation data.

Examples:

- leads
- appointments
- transcripts
- follow-up jobs
- service FAQs
- activity logs

---

# 5. Suggested Tech Stack

## Backend
- Python
- FastAPI

## Frontend
- Streamlit for fast MVP
or
- React for a production-style UI

## Database
- PostgreSQL
or
- MySQL

## AI
- OpenAI API
- optional retrieval layer for FAQ grounding

## Automation
- APScheduler / Celery for follow-up jobs
- Redis optional for queues
- n8n / Make / Zapier optional for no-code integrations

## Messaging / Telephony
- Twilio for SMS and voice
- WhatsApp Business API if expanded

## Calendar
- Google Calendar API
- Calendly API
- Acuity Scheduling API

## Deployment
- Render / Railway / VPS / Docker

---

# 6. Project Structure

A clean structure is important so the system can grow from MVP to production.

```bash
ai-receptionist/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   ├── leads.py
│   │   │   ├── bookings.py
│   │   │   ├── webhooks.py
│   │   │   └── health.py
│   │   └── schemas/
│   │       ├── chat.py
│   │       ├── lead.py
│   │       ├── booking.py
│   │       └── webhook.py
│   ├── core/
│   │   ├── security.py
│   │   ├── logging.py
│   │   ├── constants.py
│   │   └── exceptions.py
│   ├── ai/
│   │   ├── prompt_manager.py
│   │   ├── intent_router.py
│   │   ├── response_generator.py
│   │   ├── faq_retriever.py
│   │   ├── qualification_agent.py
│   │   └── handoff_detector.py
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── lead_service.py
│   │   ├── booking_service.py
│   │   ├── followup_service.py
│   │   ├── calendar_service.py
│   │   ├── notification_service.py
│   │   └── transcript_service.py
│   ├── workflows/
│   │   ├── qualify_lead.py
│   │   ├── book_appointment.py
│   │   ├── follow_up_lead.py
│   │   └── escalate_to_human.py
│   ├── integrations/
│   │   ├── openai_client.py
│   │   ├── twilio_client.py
│   │   ├── google_calendar_client.py
│   │   ├── calendly_client.py
│   │   └── email_client.py
│   ├── db/
│   │   ├── session.py
│   │   ├── base.py
│   │   ├── models/
│   │   │   ├── lead.py
│   │   │   ├── conversation.py
│   │   │   ├── appointment.py
│   │   │   ├── followup_job.py
│   │   │   └── faq.py
│   │   └── repositories/
│   │       ├── lead_repository.py
│   │       ├── conversation_repository.py
│   │       ├── appointment_repository.py
│   │       └── faq_repository.py
│   ├── scheduler/
│   │   ├── jobs.py
│   │   └── worker.py
│   └── utils/
│       ├── validators.py
│       ├── datetime_helpers.py
│       └── formatting.py
├── frontend/
│   ├── streamlit_app.py
│   └── components/
│       ├── chat_widget.py
│       ├── booking_panel.py
│       └── lead_summary.py
├── data/
│   ├── seed/
│   │   ├── faq_seed.json
│   │   └── services_seed.json
│   └── samples/
│       └── demo_conversations.json
├── prompts/
│   ├── receptionist_system_prompt.md
│   ├── qualification_prompt.md
│   ├── faq_prompt.md
│   ├── booking_prompt.md
│   └── followup_prompt.md
├── tests/
│   ├── unit/
│   │   ├── test_lead_service.py
│   │   ├── test_booking_service.py
│   │   ├── test_followup_service.py
│   │   └── test_intent_router.py
│   ├── integration/
│   │   ├── test_chat_flow.py
│   │   ├── test_calendar_integration.py
│   │   └── test_webhook_flow.py
│   └── fixtures/
│       ├── leads.json
│       └── conversations.json
├── scripts/
│   ├── seed_database.py
│   ├── create_admin_user.py
│   ├── run_local_demo.py
│   └── simulate_lead.py
├── docs/
│   ├── architecture.md
│   ├── api_contracts.md
│   ├── workflow_map.md
│   └── deployment.md
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── SKILL.md
````

---

# 7. Folder Responsibilities

## `app/main.py`

Application entry point. Starts the FastAPI server and registers routes.

## `app/api/routes/`

Contains HTTP endpoints for chat, leads, bookings, webhooks, and health checks.

## `app/api/schemas/`

Defines request and response schemas using Pydantic.

## `app/ai/`

Contains AI-specific logic such as prompt handling, intent routing, qualification flow, and FAQ support.

## `app/services/`

Contains business logic. This is where the real application behavior should live.

## `app/workflows/`

Contains multi-step workflow orchestration such as end-to-end lead qualification and booking.

## `app/integrations/`

Wraps all third-party APIs. External providers should never be called directly from route files.

## `app/db/models/`

Defines database entities.

## `app/db/repositories/`

Implements data access patterns and keeps persistence logic separate from business logic.

## `app/scheduler/`

Handles delayed follow-up tasks and reminder execution.

## `frontend/`

Contains the demo or user-facing interface.

## `prompts/`

Stores structured prompt files separately from code so prompt engineering stays maintainable.

## `tests/`

Contains automated tests for logic, integrations, and end-to-end workflows.

## `docs/`

Stores technical documentation and architecture notes.

---

# 8. Core Data Models

## Lead

Represents a person who contacted the med spa.

Suggested fields:

* id
* full_name
* phone
* email
* source_channel
* service_interest
* new_or_returning
* qualification_status
* booking_status
* lead_status
* last_contacted_at
* created_at
* updated_at

## Conversation

Stores interaction history.

Suggested fields:

* id
* lead_id
* channel
* message_role
* message_text
* intent
* confidence_score
* created_at

## Appointment

Stores booking details.

Suggested fields:

* id
* lead_id
* service_name
* appointment_datetime
* provider_name
* calendar_event_id
* booking_status
* created_at

## FollowUpJob

Tracks pending or executed follow-up actions.

Suggested fields:

* id
* lead_id
* scheduled_for
* status
* message_template
* attempt_number
* executed_at

## FAQ

Stores spa knowledge base entries.

Suggested fields:

* id
* question
* answer
* category
* active

---

# 9. Conversation Design Rules

The AI receptionist should behave as:

* polite
* concise
* warm
* professional
* conversion-focused
* never pushy
* medically cautious
* clear when it does not know something

The AI should avoid:

* pretending to be human if policy requires disclosure
* giving medical advice beyond safe business information
* inventing pricing, availability, or policies
* confirming bookings before calendar validation
* continuing uncertain flows without clarification logic

---

# 10. Workflow Layout

## 10.1 New Lead Workflow

1. Lead arrives from channel
2. System creates or updates lead record
3. AI sends greeting
4. AI detects user intent
5. Conversation continues into FAQ, qualification, or booking path

## 10.2 Qualification Workflow

1. Ask service of interest
2. Ask whether new or returning
3. Ask preferred date/time
4. Capture contact details if missing
5. Mark lead qualification status

## 10.3 Booking Workflow

1. Request available slots from calendar
2. Present top options
3. Confirm selected slot
4. Create appointment record
5. Send booking confirmation
6. Cancel pending follow-up jobs

## 10.4 Follow-Up Workflow

1. Detect abandoned conversation or no booking outcome
2. Create follow-up job
3. Send reminder at scheduled time
4. Re-open booking flow if lead responds
5. Stop after booking, opt-out, or maximum attempts

## 10.5 Human Escalation Workflow

1. Detect escalation trigger
2. Tag conversation for human review
3. notify receptionist/admin
4. send professional handoff message to lead

---

# 11. MVP Build Order

Build in this order:

## Step 1

Set up backend skeleton:

* FastAPI app
* environment config
* route registration
* database connection
* basic logging

## Step 2

Build lead and conversation models.

## Step 3

Build chat endpoint and AI response pipeline.

## Step 4

Implement FAQ answering and lead capture.

## Step 5

Implement lead qualification workflow.

## Step 6

Connect calendar and slot retrieval.

## Step 7

Implement booking confirmation flow.

## Step 8

Implement follow-up scheduler.

## Step 9

Add dashboard/demo frontend.

## Step 10

Test end-to-end flows and deploy.

---

# 12. Minimum Viable Endpoints

Suggested API routes:

## Chat

* `POST /api/chat/message`
* `GET /api/chat/history/{lead_id}`

## Leads

* `POST /api/leads`
* `GET /api/leads/{lead_id}`
* `PATCH /api/leads/{lead_id}`

## Bookings

* `GET /api/bookings/slots`
* `POST /api/bookings/create`
* `PATCH /api/bookings/{booking_id}/cancel`

## Webhooks

* `POST /api/webhooks/twilio`
* `POST /api/webhooks/whatsapp`

## Health

* `GET /api/health`

---

# 13. Environment Variables

Example `.env.example`

```env
APP_NAME=AI Receptionist
APP_ENV=development
DEBUG=true

OPENAI_API_KEY=
DATABASE_URL=
SECRET_KEY=

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

GOOGLE_CALENDAR_CREDENTIALS_PATH=
GOOGLE_CALENDAR_ID=

EMAIL_FROM=
SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
```

---

# 14. Prompt Assets

The project should keep prompts separate from logic.

## `receptionist_system_prompt.md`

Defines assistant tone, role, and boundaries.

## `qualification_prompt.md`

Guides the model through collecting lead details.

## `faq_prompt.md`

Helps answer grounded questions using available spa data.

## `booking_prompt.md`

Focuses on scheduling and slot confirmation.

## `followup_prompt.md`

Defines reminder and re-engagement style.

---

# 15. Testing Strategy

## Unit Tests

Test:

* lead qualification logic
* booking rules
* follow-up scheduling
* intent routing
* repository behavior

## Integration Tests

Test:

* API routes
* OpenAI wrapper behavior
* calendar integration
* Twilio webhook processing

## End-to-End Tests

Simulate:

* new lead asks FAQ then books
* new lead qualifies but abandons flow
* abandoned lead receives follow-up and later books
* lead requests human help

---

# 16. Deployment Layout

## Local Development

* FastAPI backend
* local database
* Streamlit frontend
* ngrok optional for webhook testing

## Cloud Deployment

* Backend API on Render/Railway/VPS
* PostgreSQL managed instance
* scheduler worker process
* Twilio webhook pointed to public backend
* frontend hosted separately if needed

---

# 17. Resume / Portfolio Positioning

This project should be presented as:

**AI Receptionist for Med Spas**
Built an AI-powered receptionist system that automates lead intake, FAQ answering, qualification, appointment booking, and follow-up workflows for appointment-based wellness businesses. Designed a modular backend with conversational AI, calendar integration, messaging workflows, and persistent lead tracking.

---

# 18. Success Criteria

The project is successful when it can:

* receive a lead
* respond immediately
* collect core lead information
* answer common business questions
* offer real appointment slots
* confirm a booking
* trigger follow-up when no booking occurs
* store the conversation and lead outcome

---

# 19. Personal Project Standard

To make this a strong personal project, it should demonstrate:

* clean architecture
* modular services
* real API integrations
* production-style folder organization
* test coverage
* clear prompts
* database-backed workflows
* deployment readiness

The project should not look like a simple chatbot demo. It should look like a real business automation system.

```

### Best structure choice for you
Because of your background, I’d recommend this stack for the first build:

- **FastAPI** for backend
- **Streamlit** for quick demo frontend
- **PostgreSQL/MySQL** for storage
- **OpenAI API** for conversation
- **Google Calendar API** for booking
- **Twilio** later for SMS/voice

That gives you a strong portfolio project without overcomplicating version one.
```