# 🧠 Nova AI Chatbot

A **context-aware AI chatbot** with Django backend and Next.js frontend. Users can configure their own Groq API key and select from available open-source models.

## Quick Start

### Backend

```bash
cd backend
.\venv\Scripts\activate    # Windows
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 to use the chatbot.

## ✨ Features

- 🔑 **Custom API Key** - Use your own Groq API key
- 🤖 **Model Selection** - Choose from Llama, Mistral, Gemma, DeepSeek, etc.
- 💬 **Context-Aware** - Remembers conversation history
- 🔐 **Secure Auth** - JWT-based authentication
- 🎨 **Modern UI** - Dark theme with responsive design

## 📚 Documentation

See [docs/README.md](docs/README.md) for detailed documentation.
