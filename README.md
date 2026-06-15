# 🛡️ Janashakthi Agent — AI-Powered Policy Endorsement Ecosystem

> An AI-centric autonomous policy servicing web application for **Janashakthi Insurance PLC**, built as part of the Independent Study in Data Science (DSC3263) at the University of Peradeniya.

---

## 📌 Overview

The **Janashakthi Agent** digitises and automates the end-to-end lifecycle of life insurance policy amendment requests — replacing the manual, paper-based branch workflow with an intelligent web platform capable of:

- Reading and verifying **multilingual handwritten documents** (Sinhala, Tamil, English)
- Classifying **handwritten Sinhala request letters** into service types
- **Auto-approving** low-risk non-financial amendments without human intervention
- Routing financial amendments to an **underwriter dashboard** for human review
- Guiding customers through the process via a **RAG-augmented AI assistant**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Two-Factor OTP Verification | NIC-based login + 6-digit email OTP with 5-minute expiry |
| 📄 Multilingual OCR Pipeline | Three-pass LLaMA 4 Scout vision model for Sinhala/Tamil/English documents |
| 🪪 NIC Mathematical Decoder | Programmatic extraction of DOB and gender from Sri Lankan NIC formats |
| 🤖 JanashakthiCare AI Assistant | RAG-augmented LLaMA 3.3 70B conversational assistant (ChromaDB + sentence-transformers) |
| ✅ Auto-Approval Engine | Automated DB update for non-financial endorsements upon AI verification |
| 📋 Underwriter Dashboard | Request queue, document review, approve/reject decisions |
| ⭐ Customer Satisfaction Rating | Post-submission 5-star widget with escalation panel for low ratings |

---

## 🗂️ Project Structure

```
janashakthi/
│
├── run.py                          # Entry point: python run.py
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
│   │   └── request_service.py      # Create, submit, auto-approve, route requests
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── views.py                # Gemini: document verification + chat
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
|   ├── js/                         # (for future separated JS)
│   └── images/            
│
├── database/
│   └── janashakthi.db              # SQLite DB (auto-created on first run)
│
└── uploads/                        # Uploaded documents (auto-created)
```

---

## ⚡ Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
python run.py
```

### 3. Access the portals

| Portal | URL |
|---|---|
| 🧑 Customer Portal | http://localhost:5000 |
| 🏢 Underwriter Dashboard | http://localhost:5000/underwriter |

---

## 🔌 API Reference

### Customer Endpoints (`/api/`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/identify` | Identify customer by NIC and/or policy number |
| POST | `/api/chat` | AI chat with customer (Gemini) |
| POST | `/api/request/create` | Create a new service request |
| POST | `/api/document/upload` | Upload and AI-verify a document |
| POST | `/api/request/submit` | Submit request for processing |

### Underwriter Endpoints (`/api/underwriter/`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/underwriter/requests?status=Under Review` | List requests by status |
| GET | `/api/underwriter/request/<id>` | Full request + document details |
| POST | `/api/underwriter/decide` | Approve or reject a request + update database |
| GET | `/api/underwriter/stats` | Dashboard statistics |

---

## 📋 Services & Document Requirements

| Service | Category | Post-Submission | Required Documents |
|---|---|---|---|
| Name Change | Non-Financial | ✅ Auto-Approved | Request Letter + NIC / Birth Cert / Marriage Cert |
| Age Alteration | Non-Financial | ✅ Auto-Approved | Request Letter + NIC / Birth Cert |
| Change Payment Mode | Financial | 🕐 Under Review | Request Letter + Outstanding Payment Bill |
| Increase of Benefits | Financial | 🕐 Under Review | Request Letter + PEP/DGF Form + Salary Slip / Bank Statement |

---

## 🧪 Test Accounts (Pre-seeded)

| NIC | Full Name | Policies |
|---|---|---|
| 881324008V | B.A.N.M. Balasooriya | LI42511344, LI44001241 |
| 971742534V | P.A.K.D. Fonseka | LI421775 |
| 756234521V | M.D. Samarawickrama | LI42514876, LI44101242 |
| 852341267V | K.L.S. Perera | LI43201234 |
| 902156789V | H.M.T. Dilrukshi | LI43301235 |
| 781234567V | R.M.N. Rathnayake | LI43401236 |
| 862345678V | S.P. Jayawardena | LI43501237 |
| 930123456V | A.B.C. Fernando | LI43601238 |
| 801234567V | D.M. Wickramasinghe | LI43701239 |
| 951234567V | N.P. Liyanage | LI43801240 |

> ⚠️ All names, NIC numbers, and contact details are fictitious and used solely for functional testing.

---

