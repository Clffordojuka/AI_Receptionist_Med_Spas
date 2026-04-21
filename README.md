# AI Receptionist for Med Spas

AI Receptionist is a modular FastAPI + Streamlit project that simulates a med spa receptionist workflow. It handles lead intake, conversational interactions, FAQ support, qualification tracking, booking, follow-up automation, human handoff, and admin review.

## Features

- Lead creation and management
- AI receptionist chat pipeline
- Conversation logging
- FAQ retrieval
- Qualification field extraction
- Slot lookup and booking flow
- Follow-up automation
- Human handoff and admin controls
- Streamlit dashboard for live demo

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Streamlit
- OpenAI-ready chat layer
- Docker-friendly PostgreSQL setup

## Project Structure

- `app/` backend application
- `frontend/` Streamlit demo dashboard
- `scripts/` seed and demo utilities
- `prompts/` AI prompt assets
- `tests/` unit and integration tests

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Configure environment

Create `.env` in project root:

```env
APP_NAME=AI Receptionist
APP_ENV=development
DEBUG=true
API_V1_PREFIX=/api
DATABASE_URL=postgresql+psycopg://postgres:amani_admin@localhost:5433/postgres
SECRET_KEY=super-secret-key
OPENAI_API_KEY=
```

### 3. Start PostgreSQL with Docker

```bash
docker run --name receptionist_db -e POSTGRES_PASSWORD=amani_admin -p 5433:5432 -d postgres
```

### 4. Start FastAPI

```bash
uvicorn app.main:app --reload
```

### 5. Start Streamlit

```bash
streamlit run frontend/streamlit_app.py
```

## Demo Utilities

Seed demo data:

```bash
python scripts/seed_demo_data.py
```

Run a sample workflow:

```bash
python scripts/demo_workflow.py
```

## Core API Areas

* `/api/leads`
* `/api/chat`
* `/api/bookings`
* `/api/followups`
* `/api/admin`
* `/api/dashboard`

## MVP Status

This project currently supports a full receptionist-style workflow for demo and portfolio use, with modular boundaries in place for future real integrations such as Google Calendar, Twilio SMS, WhatsApp, and production-grade job scheduling.

````