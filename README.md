# AI-Centric-Ecosystem-Janashakthi-Insuarance

## Project Structure
janashakthi/
│
├── run.py                          # ← Entry point: python run.py
├── requirements.txt
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Flask config (dev/prod), API keys, paths
│
├── app/
│   ├── __init__.py                 # App factory (create_app)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py             # SQLite setup, seed data, db_connection()
│   │   └── constants.py            # SERVICE_REQUIREMENTS, DOC_LABELS
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py           # Gemini: document verification + chat
│   │   ├── customer_service.py     # Customer lookup by NIC / policy number
│   │   └── request_service.py      # Create, submit, approve/reject requests
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── views.py                # Serves HTML pages + uploads
│   │   ├── customer.py             # /api/identify, /api/chat, /api/request/*
│   │   ├── documents.py            # /api/document/upload
│   │   └── underwriter.py          # /api/underwriter/*
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py              # allowed_file(), save_uploaded_file(), success(), error()
│
├── templates/
│   ├── customer.html               # Customer chatbot portal
│   └── underwriter.html            # Underwriter dashboard
│
├── static/
│   ├── css/                        # (for future separated CSS)
│   ├── js/                         # (for future separated JS)
│   └── images/
│
├── database/
│   └── janashakthi.db              # SQLite DB (auto-created on first run)
│
└── uploads/                        # Uploaded documents (auto-created)

## Quick Start
### 1. Install dependencies
pip install -r requirements.txt
