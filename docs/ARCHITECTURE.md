# 🏗️ System Architecture

This document describes the high-level architecture of the Nova AI Chatbot.

---

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                         │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js + React)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  AuthContext │  │  Chat Page  │  │  Sidebar Component     │  │
│  │  (JWT Auth)  │  │  (Messages) │  │  (API Key + Models)    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                   │
                            HTTP/REST API
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Django REST Framework)               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Auth Views  │  │  Chat Views │  │  API Key Management    │  │
│  │  (JWT)       │  │  (Messages) │  │  (Encrypt/Decrypt)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    LangChain Service                       │  │
│  │  • Session Memory (RunnableWithMessageHistory)             │  │
│  │  • System Prompt (Nova personality)                        │  │
│  │  • Model Selection (user's choice)                         │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                   │
                            Groq API (HTTPS)
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                       GROQ LPU CLOUD                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Open Source Models: Llama 3.3, Mistral, Gemma, etc.    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### Frontend (Next.js 16)

| Component       | File                     | Purpose                                  |
| --------------- | ------------------------ | ---------------------------------------- |
| **AuthContext** | `context/AuthContext.js` | Manages JWT tokens, login/logout state   |
| **Chat Page**   | `app/chat/page.js`       | Main chat interface with message display |
| **Sidebar**     | `components/Sidebar.js`  | API key input and model selection        |
| **API Client**  | `lib/api.js`             | Axios instance with JWT interceptors     |

### Backend (Django 5.x)

| Component       | File                     | Purpose                                     |
| --------------- | ------------------------ | ------------------------------------------- |
| **Models**      | `chatbot/models.py`      | `Chat`, `UserAPIKey` database models        |
| **Services**    | `chatbot/services.py`    | LangChain integration, encryption, Groq API |
| **API Views**   | `chatbot/api_views.py`   | REST endpoints for chat, auth, settings     |
| **Serializers** | `chatbot/serializers.py` | Request/response data validation            |

---

## Data Flow

### 1. User Sends Message

```
User Input → Frontend → POST /api/chat/ → Backend
                                            │
                        ┌───────────────────┴───────────────────┐
                        │ 1. Validate JWT token                  │
                        │ 2. Get user's API key (decrypt)        │
                        │ 3. Get user's selected model           │
                        │ 4. Load session history (LangChain)    │
                        │ 5. Call Groq API with context          │
                        │ 6. Save message + response to DB       │
                        │ 7. Return response                     │
                        └───────────────────────────────────────┘
                                            │
                                            ▼
                                   JSON Response → Frontend → Display
```

### 2. Context Memory

```
Session Store (In-Memory Dict)
│
├── "user_1_session_abc" → ChatMessageHistory
│   ├── HumanMessage: "Who is Elon Musk?"
│   ├── AIMessage: "Elon Musk is..."
│   ├── HumanMessage: "What companies did he found?"
│   └── AIMessage: "He founded Tesla, SpaceX..."  ← Context aware!
│
└── "user_2_session_xyz" → ChatMessageHistory
    └── ...
```

---

## Security Architecture

### API Key Encryption

```
User enters API key → Fernet Encrypt → Store in DB (encrypted)
                           │
                     ENCRYPTION_KEY
                     (from .env)
                           │
                           ▼
Request comes in → Fernet Decrypt → Use for Groq API call
```

### JWT Authentication

```
Login → Generate Access + Refresh tokens
            │
            ▼
Access Token (15 min) ──→ Authorization header
            │
            ▼ (expired)
Refresh Token (7 days) ──→ Get new Access Token
```

---

## Directory Structure

```
chatbot-react/
├── backend/                    # Django Backend
│   ├── chatbot/                # Main Django app
│   │   ├── models.py           # Database models
│   │   ├── views.py            # Template views (legacy)
│   │   ├── api_views.py        # REST API views
│   │   ├── serializers.py      # DRF serializers
│   │   ├── services.py         # LangChain + Groq logic
│   │   └── urls.py             # URL routing
│   ├── chatbot_project/        # Django project settings
│   ├── templates/              # HTML templates (legacy)
│   ├── manage.py
│   ├── requirements.txt
│   ├── system_prompt.txt       # Nova AI personality
│   └── .env                    # Environment variables
│
├── frontend/                   # Next.js Frontend
│   ├── app/                    # Next.js pages
│   │   ├── chat/page.js        # Chat interface
│   │   ├── login/page.js       # Login page
│   │   └── register/page.js    # Registration page
│   ├── components/             # React components
│   │   └── Sidebar.js          # Settings sidebar
│   ├── context/                # React contexts
│   │   └── AuthContext.js      # Auth state management
│   ├── lib/                    # Utilities
│   │   └── api.js              # Axios client
│   └── package.json
│
└── docs/                       # Documentation
```

---

## Technology Choices

| Decision               | Choice    | Reason                                 |
| ---------------------- | --------- | -------------------------------------- |
| **Backend Framework**  | Django    | Mature, batteries-included, great ORM  |
| **API Framework**      | DRF       | Standard for Django REST APIs          |
| **Frontend Framework** | Next.js   | Server components, great DX            |
| **LLM Framework**      | LangChain | Easy memory management, prompts        |
| **LLM Provider**       | Groq      | Fast inference, free tier, open models |
| **Auth**               | JWT       | Stateless, scalable, industry standard |
| **Encryption**         | Fernet    | Symmetric, secure, built into Python   |
