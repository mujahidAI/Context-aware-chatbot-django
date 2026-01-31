# 🚀 Getting Started

Get the Nova AI Chatbot running on your machine in under 10 minutes.

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **Groq API Key** (free) - [Get one here](https://console.groq.com/keys)

---

## Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/chatbot-react.git
cd chatbot-react
```

### 2. Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy the example and edit with your values
```

Create `backend/.env`:

```env
GROQ_API_KEY=gsk_your_api_key_here
ENCRYPTION_KEY=your_fernet_key_here
SECRET_KEY=your_django_secret_key
DEBUG=True
```

> 💡 **Generate an encryption key:**
>
> ```python
> from cryptography.fernet import Fernet
> print(Fernet.generate_key().decode())
> ```

```bash
# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

✅ Backend running at `http://localhost:8000`

---

### 3. Setup Frontend

Open a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at `http://localhost:3000`

---

## First Steps

1. **Open the app** - Go to `http://localhost:3000`

2. **Register an account**

   - Click "Sign Up"
   - Enter username, email, password
   - You'll be logged in automatically

3. **Configure your API key**

   - Click the ⚙️ settings button in the header
   - Enter your Groq API key
   - Click "Save API Key"

4. **Start chatting!**
   - Type a message and press Enter
   - Nova will respond using your selected model

---

## Optional: Create a Superuser

To access Django admin:

```bash
cd backend
python manage.py createsuperuser
```

Then visit `http://localhost:8000/admin/`

---

## Troubleshooting

### "CORS Error" in browser console

Make sure both servers are running:

- Backend on port 8000
- Frontend on port 3000

### "No module named 'xyz'"

```bash
cd backend
pip install -r requirements.txt
```

### "npm ERR! ENOENT"

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database errors

```bash
cd backend
python manage.py migrate
```

---

## Next Steps

- 📖 [Environment Setup](environment-setup.md) - Detailed configuration options
- 🔌 [API Reference](../api/endpoints.md) - Explore the API
- 🏗️ [Architecture](../ARCHITECTURE.md) - Understand the codebase
