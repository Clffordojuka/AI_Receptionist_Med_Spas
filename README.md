# AI Receptionist for Med Spas

AI Receptionist is a full-stack workflow automation project built with FastAPI, PostgreSQL, and Streamlit. It is designed to simulate how a modern med spa receptionist can handle lead intake, answer common questions, qualify clients, support appointment booking, automate follow-ups, and route sensitive conversations to human staff when needed.

The project is structured as a modular, API-driven system with a demo dashboard that makes it easy to test, present, and extend.

---

## Overview

This project was built to model a realistic receptionist workflow for appointment-based businesses such as med spas, aesthetic clinics, and wellness centers.

It supports the full lead journey:

- lead capture
- receptionist-style conversation handling
- FAQ support
- qualification data extraction
- booking flow and appointment creation
- follow-up scheduling
- human handoff and admin review
- dashboard-based monitoring and interaction

Rather than building a simple chatbot demo, the goal of this project is to present a more complete operational workflow that reflects how an AI receptionist could support a real business environment.

---

## Key Features

- Lead creation and lead lifecycle management
- AI receptionist chat pipeline
- Conversation logging and transcript history
- FAQ retrieval from stored business knowledge
- Automatic extraction of qualification details from messages
- Appointment slot lookup and booking flow
- Follow-up scheduling and abandoned lead recovery
- Human handoff detection and escalation support
- Admin workflow controls and lead review tools
- Streamlit dashboard for demo and interactive testing
- Alembic-based schema migration support
- Docker Compose setup for full local environment startup

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic

### Frontend
- Streamlit
- Pandas
- Requests

### Infrastructure
- Docker
- Docker Compose

### AI Layer
- OpenAI-ready chat response layer
- Rule-based intent routing
- Qualification extraction
- FAQ grounding logic

---

## Project Structure

```bash
ai_receptionist/
├── app/
│   ├── api/
│   ├── ai/
│   ├── core/
│   ├── db/
│   ├── integrations/
│   ├── scheduler/
│   ├── services/
│   ├── workflows/
│   ├── config.py
│   ├── dependencies.py
│   └── main.py
├── frontend/
│   ├── components/
│   └── streamlit_app.py
├── scripts/
│   ├── seed_demo_data.py
│   ├── seed_database.py
│   └── demo_workflow.py
├── alembic/
├── prompts/
├── tests/
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── requirements.txt
├── .env
└── README.md
````

---

## System Capabilities

The current MVP supports the following workflow:

### Lead Intake

New leads can be created and tracked through the backend API or Streamlit dashboard.

### Chat and Conversation Logging

The receptionist can receive messages, classify intent, generate responses, and store both user and assistant messages in conversation history.

### FAQ Handling

The system can respond to common business questions using stored FAQ records rather than relying only on generic fallback responses.

### Qualification Flow

Lead information such as name, phone number, email, client type, and service interest can be extracted from natural conversation and saved back to the lead record.

### Booking Flow

The system supports available slot lookup, booking creation, appointment persistence, and lead status updates.

### Follow-Up Automation

Follow-up jobs can be created, scheduled, executed, logged, and cancelled when a lead books successfully.

### Human Handoff

The receptionist can detect escalation cases, flag the lead for staff review, and support admin-side notes and assignment.

### Dashboard Workflow

The Streamlit frontend provides a receptionist-style workspace for interacting with leads, reviewing chats, bookings, follow-ups, and admin controls.

---

## Local Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create the environment file

Create a `.env` file in the project root.

Example:

```env
APP_NAME=AI Receptionist
APP_ENV=development
DEBUG=true
API_V1_PREFIX=/api

DATABASE_URL=postgresql+psycopg://postgres:amani_admin@localhost:5433/ai_receptionist_db
SECRET_KEY=super-secret-key
OPENAI_API_KEY=

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

### 3. Start PostgreSQL with Docker

```bash
docker run --name receptionist_db -e POSTGRES_PASSWORD=amani_admin -e POSTGRES_DB=ai_receptionist_db -p 5433:5432 -d postgres
```

### 4. Apply database migrations

```bash
alembic upgrade head
```

### 5. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

### 6. Start the Streamlit frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

## Run with Docker Compose

You can start the full stack with Docker Compose.

### Start all services

```bash
docker compose up --build
```

This starts:

* PostgreSQL
* FastAPI backend
* Streamlit frontend

### Stop services

```bash
docker compose down
```

### Stop services and remove volumes

```bash
docker compose down -v
```

### Apply migrations manually inside backend container

```bash
docker compose exec backend alembic upgrade head
```

### Seed demo data inside backend container

```bash
docker compose exec backend python scripts/seed_demo_data.py
```

### Run the sample workflow inside backend container

```bash
docker compose exec backend python scripts/demo_workflow.py
```

---

## Demo Utilities

### Seed demo data

This populates the database with sample FAQs, leads, conversations, and follow-up jobs for dashboard testing.

```bash
python scripts/seed_demo_data.py
```

### Run a sample workflow

This script creates a lead, sends a sample chat message, checks slots, creates a booking, and fetches the admin review summary.

```bash
python scripts/demo_workflow.py
```

---

## Core API Areas

* `/api/leads`
* `/api/chat`
* `/api/faqs`
* `/api/bookings`
* `/api/followups`
* `/api/admin`
* `/api/dashboard`

---

## Alembic Migration Workflow

This project uses Alembic for database schema management.

### Create a new migration after model changes

```bash
alembic revision --autogenerate -m "describe your change"
```

### Apply migrations

```bash
alembic upgrade head
```

### Check current revision

```bash
alembic current
```

For the current project setup, Alembic should be used for schema evolution instead of relying on `Base.metadata.create_all()` during application startup.

---

## Current MVP Status

The current MVP supports a complete receptionist-style flow for local demo and portfolio presentation:

* create and manage leads
* chat with the receptionist
* answer FAQ-style questions
* extract qualification details
* create appointments
* schedule and run follow-ups
* escalate to human review
* manage leads from a dashboard

The system is modular enough to support the next upgrades without major restructuring.

---

## Next Upgrade Paths

The strongest next production-oriented extensions are:

* real Google Calendar integration
* Twilio SMS integration
* WhatsApp workflow support
* authentication and admin login
* production deployment configuration
* queue-based background job execution

---

## Why This Project Matters

This project demonstrates more than chatbot logic. It shows how conversational AI, workflow orchestration, persistence, admin tooling, and frontend interaction can be combined into a usable business workflow system.

It is designed to showcase practical backend engineering, API design, AI-assisted workflow handling, and product-minded system architecture in one project.

```