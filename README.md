# 🧑‍💻 Django AI Chatbot

A **Django-based AI chatbot** that integrates with an open-source LLM to provide **context-aware conversations**, **multi-session chat history**, and **secure user authentication**.

This project combines **full-stack web development** with **Generative AI**, creating a chatbot experience similar to ChatGPT — but powered entirely by free, open-source tools.

## 🚀 Features

- **Open-Source LLM Integration** – Uses a completely free model (no API costs)
- **Context-Aware Conversations** – Remembers past interactions for smooth, natural chats
- **Secure Authentication** – User login, signup, and email-based password reset
- **Personalized Chat History** – Stores each user's conversations for future reference
- **Multi-Session Support** – Start fresh chats in new sessions (like ChatGPT's sidebar)
- **Responsive Design** – Works seamlessly on desktop and mobile devices
- **Real-time Chat Interface** – Smooth, interactive messaging experience

## 🛠️ Tech Stack

- **Backend**: Django 4.x, Django ORM
- **Frontend**: HTML5, CSS3, JavaScript (Django templates)
- **Database**: SQLite (default, easily swappable with PostgreSQL/MySQL)
- **AI Model**: Open-source LLM (integrated via API wrapper)
- **Authentication**: Django's built-in auth system with custom enhancements
- **Styling**: Bootstrap 5 (optional) or custom CSS

## 📂 Project Structure

```
django-chatbot/
├── chatbot/                 # Main chatbot app
│   ├── models.py            # Chat & user-related models
│   ├── views.py             # Chat logic & API endpoints
│   ├── urls.py              # App URL patterns
│   ├── forms.py             # Authentication forms
│   ├── admin.py             # Django admin configuration
│   ├── templates/           # Frontend templates
│   │   ├── chatbot/
│   │   │   ├── chat.html
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── base.html
│   ├── static/              # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── migrations/          # Database migrations
├── chatbot_project/         # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/               # Global templates
├── static/                  # Global static files
├── media/                   # User-uploaded files
├── requirements.txt
├── manage.py
├── .env.example
└── README.md
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/django-chatbot.git
cd django-chatbot
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env
```

Edit the `.env` file with your configurations:

```ini
# Django Settings
SECRET_KEY=your-super-secret-django-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AI Model Configuration
LLM_API_URL=http://localhost:8000/generate  # Your local LLM endpoint
LLM_API_KEY=your-api-key-if-required
LLM_MODEL_NAME=your-model-name

# Optional: Third-party integrations
OPENAI_API_KEY=your-openai-key-for-fallback
```

### 5. Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser
```

### 6. Collect Static Files (for production)

```bash
python manage.py collectstatic
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to start chatting!

## 🔧 Configuration

### LLM Integration

The chatbot can work with various open-source LLMs. Configure your preferred model in `chatbot/llm_integration.py`:

```python
# Example configurations for popular open-source models
LLM_CONFIGS = {
    'ollama': {
        'base_url': 'http://localhost:11434',
        'model': 'llama2'
    },
    'text-generation-webui': {
        'base_url': 'http://localhost:5000',
        'model': 'your-model-name'
    }
}
```

### Database Migration (PostgreSQL)

For production, switch to PostgreSQL:

```bash
pip install psycopg2-binary
```

Update `.env`:
```ini
DATABASE_URL=postgresql://username:password@localhost:5432/chatbot_db
```

## 🧪 Testing the Chatbot

### Context Awareness Tests

Try these conversation sequences to test memory retention:

1. **Personal Information**:
   - "My name is John and I live in New York."
   - "What's my name?" → Should remember "John"
   - "Where do I live?" → Should remember "New York"

2. **Mathematical Context**:
   - "What is 15 + 25?"
   - "Multiply that result by 3" → Should use previous answer (40)

3. **Topic Continuity**:
   - "Tell me about Python programming."
   - "What are its main advantages?" → Should continue Python discussion

### User Authentication Tests

- Register new account
- Login/logout functionality
- Password reset via email
- Chat history persistence across sessions

## 📱 Usage Examples

### Starting a Conversation

```python
# In Django shell (python manage.py shell)
from chatbot.models import ChatSession, ChatMessage
from django.contrib.auth.models import User

# Create a new chat session
user = User.objects.get(username='your_username')
session = ChatSession.objects.create(user=user, title="Test Chat")

# Send a message
message = ChatMessage.objects.create(
    session=session,
    message="Hello, how are you?",
    is_user=True
)
```

### API Endpoints

- `GET /` - Main chat interface
- `POST /chat/` - Send message to chatbot
- `GET /chat/history/` - Retrieve chat history
- `POST /chat/new-session/` - Start new chat session
- `DELETE /chat/session/<id>/` - Delete chat session

## 🚀 Deployment

### Using Railway

1. Fork this repository
2. Connect to Railway
3. Add environment variables
4. Deploy automatically

### Using Render

1. Create new web service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn chatbot_project.wsgi:application`

### Docker Deployment

```dockerfile
# Dockerfile included in repository
docker build -t django-chatbot .
docker run -p 8000:8000 django-chatbot
```

## 📊 Features Roadmap

### Completed ✅
- Basic chat functionality
- User authentication
- Chat history storage
- Context awareness
- Multi-session support

### Planned 🚧
- **RAG Integration** - Upload documents for Q&A
- **Real-time Streaming** - Live response generation
- **Voice Chat** - Speech-to-text and text-to-speech
- **Chat Export** - Download conversations as PDF/JSON
- **Admin Dashboard** - Monitor usage and conversations
- **API Documentation** - Swagger/OpenAPI integration
- **Mobile App** - React Native companion app

### Future Ideas 💡
- Multi-language support
- Chat sharing functionality
- Integration with external APIs
- Custom chatbot personas
- Analytics dashboard

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Ensure backward compatibility

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No module named 'chatbot'"
**Solution**: Make sure you're in the correct directory and virtual environment is activated

**Issue**: Database errors
**Solution**: Run `python manage.py migrate` to apply migrations

**Issue**: Static files not loading
**Solution**: Run `python manage.py collectstatic` and check `STATIC_URL` settings

**Issue**: LLM not responding
**Solution**: Check your LLM service is running and API configuration is correct

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the robust web framework
- Open-source LLM developers for making AI accessible
- Contributors who help improve this project

## 📞 Support

- 📧 Email: your-email@example.com
- 💬 Discord: [Join our server](https://discord.gg/your-invite)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/django-chatbot/issues)

---

⚡ **Built with Django + Open-Source AI to explore the future of conversational agents.**

*Star ⭐ this repo if you found it helpful!*
