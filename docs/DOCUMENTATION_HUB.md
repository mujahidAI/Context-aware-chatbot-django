# 📚 Nova AI Chatbot - Documentation Hub

Welcome to the Nova AI Chatbot documentation! This hub provides everything you need to understand, set up, and contribute to the project.

---

## 🚀 Quick Links

| Section                                          | Description                          |
| ------------------------------------------------ | ------------------------------------ |
| [Getting Started](guides/getting-started.md)     | Quick setup guide for new developers |
| [Environment Setup](guides/environment-setup.md) | Detailed environment configuration   |
| [API Overview](api/overview.md)                  | Understanding the REST API           |
| [API Endpoints](api/endpoints.md)                | Complete API reference               |
| [Database Schema](database/schema.md)            | Models and relationships             |
| [Architecture](ARCHITECTURE.md)                  | System design and tech stack         |

---

## 📂 Documentation Structure

```
docs/
├── api/                    # API Documentation
│   ├── overview.md         # API architecture & authentication
│   └── endpoints.md        # Complete endpoint reference
│
├── database/               # Database Documentation
│   ├── schema.md           # Models and field descriptions
│   └── ERD.png             # Entity Relationship Diagram
│
├── deployment/             # Deployment Guides
│   ├── render.md           # Deploy backend to Render
│   ├── railway.md          # Deploy backend to Railway
│   └── vercel.md           # Deploy frontend to Vercel
│
├── guides/                 # Developer Guides
│   ├── getting-started.md  # Quick start tutorial
│   └── environment-setup.md # Detailed setup instructions
│
├── ARCHITECTURE.md         # System architecture
├── CODE_OF_CONDUCT.md      # Community guidelines
├── contributing.md         # How to contribute
└── DOCUMENTATION_HUB.md    # This file
```

---

## 🎯 Project Overview

**Nova AI Chatbot** is a context-aware conversational AI powered by open-source LLMs via Groq. Key features:

- 🔑 **Custom API Keys** - Users bring their own Groq API key
- 🤖 **Model Selection** - Choose from Llama, Mistral, Gemma, DeepSeek
- 💬 **Context Memory** - Remembers conversation history
- 🔐 **JWT Authentication** - Secure user sessions
- ⚡ **Fast Responses** - Powered by Groq's LPU inference

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
| ------------ | ----------------------------------- |
| **Backend**  | Django 5.x, Django REST Framework   |
| **Frontend** | Next.js 16, React 19                |
| **AI/LLM**   | LangChain, Groq API (Llama 3.3 70B) |
| **Database** | SQLite (dev) / PostgreSQL (prod)    |
| **Auth**     | JWT via SimpleJWT                   |

---

## 📖 Reading Order for New Developers

1. **[Getting Started](guides/getting-started.md)** - Get the project running locally
2. **[Architecture](ARCHITECTURE.md)** - Understand the system design
3. **[API Overview](api/overview.md)** - Learn how the API works
4. **[Database Schema](database/schema.md)** - Understand the data models
5. **[Contributing](contributing.md)** - Ready to contribute!

---

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](contributing.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting PRs.

---

## 📄 License

This project is licensed under the MIT License.
