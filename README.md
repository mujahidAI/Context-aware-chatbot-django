# 🧑‍💻 Django AI Chatbot

A **Django-based AI chatbot** that integrates with an open-source LLM to provide **context-aware conversations**, **multi-session chat history**, and **secure user authentication**.

## 🚀 Features

- **Open-Source LLM Integration** – Uses a completely free model (no API costs)
- **Context-Aware Conversations** – Remembers past interactions for smooth, natural chats
- **Secure Authentication** – User login, signup, and email-based password reset
- **Personalized Chat History** – Stores each user's conversations for future reference
- **Multi-Session Support** – Start fresh chats in new sessions

## 🛠️ Tech Stack

- **Backend**: Django, Django ORM
- **Frontend**: HTML, CSS, JavaScript (Django templates)
- **Database**: SQLite (default, can be swapped with PostgreSQL/MySQL)
- **AI Model**: Open-source LLM (integrated via API wrapper)
- **Authentication**: Django's built-in auth system

## 📂 Project Structure

```
chatbot_project/
├── chatbot/                 # Main chatbot app
│   ├── models.py            # Chat & user-related models
│   ├── views.py             # Chat logic & API endpoints
│   ├── templates/           # Frontend templates
│   └── static/              # Static assets (CSS/JS)
├── chatbot_project/         # Project settings
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/django-chatbot.git
cd django-chatbot
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment configuration

Create a `.env` file:

```ini
SECRET_KEY=your-django-secret-key
DEBUG=True
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
LLM_API_KEY=your-llm-api-key
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to start chatting!

## 🧪 Testing Context Awareness

Example queries to test memory:
1. "Who is Elon Musk?" → "What companies has he founded?"
2. "I was born in Lahore." → "What's the weather like there?"
3. "What is 10 + 5?" → "Multiply that by 2."

## 📌 Roadmap

- Add **RAG (Retrieval-Augmented Generation)** for document Q&A
- Implement **real-time streaming responses**
- Add **UI/UX improvements** (chat bubbles, dark mode, etc.)
- Deploy on **Render / Railway / Vercel + Supabase**

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to add.

## 📜 License

This project is licensed under the **MIT License** – feel free to use, modify, and distribute.

⚡ Built with **Django + Open-Source AI** to explore the future of conversational agents.
