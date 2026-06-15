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
│   └── settings.py                 # Flask config, API keys, paths
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
│   │   ├── ai_service.py           # OCR, document verification, RAG chat
│   │   ├── customer_service.py     # Customer lookup by NIC / policy number
│   │   └── request_service.py      # Create, submit, auto-approve, route requests
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── views.py                # Serves HTML pages
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
├── knowledge_base/                 # 15 ChromaDB entries for RAG retrieval
│
├── database/
│   └── janashakthi.db              # SQLite DB (auto-created on first run)
│
└── uploads/                        # Uploaded documents (auto-created)
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/nuwanihitibandara211-wq/Janashakthi-Agent.git
cd Janashakthi-Agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file or export directly:

```bash
export GROQ_API_KEY=your_groq_api_key_here
export EMAIL_ADDRESS=your_gmail_address
export EMAIL_PASSWORD=your_gmail_app_password
```

> **Gmail**: Use an [App Password](https://support.google.com/accounts/answer/185833), not your account password.

### 4. Run the server

```bash
python run.py
```

### 5. Access the portals

| Portal | URL |
|---|---|
| 🧑 Customer Portal | http://localhost:5000 |
| 🏢 Underwriter Dashboard | http://localhost:5000/underwriter |

---

## 🔌 API Reference

### Customer Endpoints (`/api/`)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/identify` | Identify customer by NIC number |
| POST | `/api/send-otp` | Generate and dispatch OTP to registered email |
| POST | `/api/verify-otp` | Validate OTP entered by customer |
| POST | `/api/chat` | Send message to JanashakthiCare AI assistant |
| POST | `/api/request/create` | Create a new service request |
| POST | `/api/document/upload` | Upload and AI-verify a document |
| POST | `/api/request/submit` | Submit request for processing |

### Underwriter Endpoints (`/api/underwriter/`)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/underwriter/requests` | List requests by status |
| GET | `/api/underwriter/request/<id>` | Full request + document details |
| POST | `/api/underwriter/decide` | Approve or reject a request |
| GET | `/api/underwriter/stats` | Dashboard statistics |

All endpoints return a consistent JSON envelope:

```json
{ "success": true, "data": { ... } }
{ "success": false, "error": "Descriptive error message" }
```

---

## 📋 Services & Document Requirements

| Service | Category | Post-Submission | Required Documents |
|---|---|---|---|
| Name Change | Non-Financial | ✅ Auto-Approved | Request Letter + NIC / Birth Cert / Marriage Cert |
| Age Alteration | Non-Financial | ✅ Auto-Approved | Request Letter + NIC / Birth Cert |
| Change Payment Mode | Financial | 🕐 Under Review | Request Letter + Outstanding Payment Bill |
| Increase of Benefits | Financial | 🕐 Under Review | Request Letter + PEP/DGF Form + Salary Slip / Bank Statement |

---

## 🤖 AI Pipeline

### 1. Identity Document OCR (NIC & Birth Certificate)

```
Step 1 → Document type detection       (LLaMA 4 Scout vision)
Step 2 → Multilingual field extraction (LLaMA 4 Scout vision → structured JSON)
Step 3 → NIC mathematical decoding     (custom Python logic)
Step 4 → Field reconciliation          (merged identity JSON)
```

**Birth Certificate three-pass pipeline:**
- **Pre-processing** — Pillow upscale (min 1400px), contrast ×1.9, sharpness ×2.2
- **Pass 1** — Full form field extraction (Sinhala + English)
- **Pass 2** — Sinhala handwriting deep-read (vowel diacritic focus)
- **Pass 3** — Merge and reconciliation with confidence notes

### 2. Request Letter Classification

```
Step 1 → Full text OCR               (LLaMA 4 Scout vision)
Step 2 → Keyword scoring             (50–80 keywords per service type)
Step 3 → Threshold filtering         (≥10% match ratio retained)
Step 4 → LLM verification            (LLaMA 3.3 70B → verified service type + confidence)
```

### 3. RAG-Augmented Conversational Assistant

- **Vector store**: ChromaDB with 15 indexed Janashakthi knowledge base entries
- **Embedding model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Retrieval**: Top-3 cosine similarity matches injected into system prompt
- **LLM**: LLaMA 3.3 70B via Groq API
- **Latency**: < 2 seconds average response time

---

## 🪪 NIC Decoding Reference

| Format | Structure | Gender Rule |
|---|---|---|
| Old format (9 digits + V/X) | Digits 1–2: birth year (1900+n); Digits 3–5: day of year | Day > 500 → Female (subtract 500) |
| New format (12 digits) | Digits 1–4: full birth year; Digits 5–7: day of year | Day > 500 → Female (subtract 500) |

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

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| flask | 3.0.0 | Web framework and REST API |
| flask-cors | 4.0.0 | Cross-Origin Resource Sharing |
| groq | latest | Groq API client (LLaMA vision + language models) |
| pillow | latest | Image pre-processing for OCR pipeline |
| pytesseract | latest | Supplemental English OCR fallback |
| chromadb | latest | Vector database for RAG knowledge base |
| sentence-transformers | latest | Sentence embedding (all-MiniLM-L6-v2) |
| werkzeug | 3.0.1 | WSGI utilities, file handling |
| python | 3.10+ | Runtime environment |

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 📊 Test Results Summary

| Document Type | Accuracy |
|---|---|
| NIC — printed | 100% |
| Bank Statement — typed | 100% |
| Marriage Certificate — printed | 100% |
| Request Letter — typed | 90% |
| PEP/DGF Form — typed | 88% |
| Birth Certificate — handwritten | 60% |
| Request Letter — handwritten | 40% |
| **Overall** | **83%** |

---

## ⚠️ Known Limitations

- Handwritten Sinhala OCR accuracy is variable for cursive/informal scripts
- Underwriter portal has no authentication (URL-accessible) — not production-ready
- OTP delivered via email only; no SMS fallback
- OTP store is in-memory and does not persist across server restarts
- SQLite not suitable for high-concurrency production deployments
- AI pipeline depends entirely on Groq API availability

---

## 🚀 Future Directions

- SMS-based OTP and biometric authentication
- Fine-tuned Sinhala handwriting OCR model
- PostgreSQL migration for production scalability
- JWT-based role-based access control (customer / branch officer / underwriter)
- Redis-based distributed OTP caching
- Expanded service coverage (reinstatement, claims, beneficiary changes)
- Native mobile app (iOS & Android)
- Analytics and reporting dashboard

---

## 👩‍💻 Authors

Developed by students of the **Department of Statistics and Computer Science**, Faculty of Science, University of Peradeniya, as part of **DSC3263 — Independent Study in Data Science** (2026).

---

## 📄 License

This project was developed for academic purposes in collaboration with **Janashakthi Insurance PLC**. No real customer data was used. All test records are entirely fictitious.

### 1. Install dependencies
pip install -r requirements.txt
