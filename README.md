# 🧑‍💻 Django AI Chatbot

A **Django-based AI chatbot** that integrates with an open-source LLM to provide **context-aware conversations**, **multi-session chat history**, and **secure user authentication**. Now featuring a **Next.js Frontend**.

## 🚀 Features

- **Open-Source LLM Integration** – Uses a completely free model (no API costs)
- **Context-Aware Conversations** – Remembers past interactions for smooth, natural chats
- **Secure Authentication** – User login, signup, and email-based password reset (JWT based)
- **Personalized Chat History** – Stores each user's conversations for future reference
- **Multi-Session Support** – Start fresh chats in new sessions
- **Modern Frontend** – Built with Next.js for a responsive and dynamic user experience.

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: Next.js, React, Bootstrap
- **Database**: SQLite (default, can be swapped with PostgreSQL/MySQL)
- **AI Model**: Open-source LLM (integrated via API wrapper)
- **Authentication**: JWT (JSON Web Tokens)

## 📂 Project Structure

```
chatbot_project/
├── chatbot/                 # Main chatbot app
│   ├── models.py            # Chat & user-related models
│   ├── api_views.py         # API endpoints
│   ├── services.py          # Chat logic
│   └── ...
├── frontend/                # Next.js Frontend
│   ├── app/                 # App Router pages
│   ├── context/             # React Context (Auth)
│   ├── lib/                 # Utilities (API client)
│   └── ...
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

### 2. Set up Backend (Django)

#### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Environment configuration

Create a `.env` file in the root directory:

```ini
SECRET_KEY=your-django-secret-key
DEBUG=True
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
GROQ_API_KEY=your-groq-api-key
```

#### Run database migrations

```bash
python manage.py migrate
```

#### Create a superuser

```bash
python manage.py createsuperuser
```

#### Run the Django development server

```bash
python manage.py runserver
```

The backend API will be available at `http://127.0.0.1:8000`.

### 3. Set up Frontend (Next.js)

Open a new terminal window and navigate to the `frontend` directory:

```bash
cd frontend
```

#### Install Node.js dependencies

```bash
npm install
```

#### Run the Next.js development server

```bash
npm run dev
```

Visit `http://localhost:3000` to start chatting!

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
