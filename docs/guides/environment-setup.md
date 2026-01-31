# ⚙️ Environment Setup

Detailed guide for configuring your development environment.

---

## Environment Variables

### Backend (`backend/.env`)

Create a `.env` file in the `backend/` directory:

```env
# === REQUIRED ===

# Django secret key (generate a random string)
SECRET_KEY=your-super-secret-django-key-here

# Groq API key (fallback when user hasn't configured their own)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Fernet encryption key for securing user API keys
ENCRYPTION_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=

# === OPTIONAL ===

# Debug mode (set to False in production)
DEBUG=True

# Database configuration (only needed for PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nova_chatbot
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Allowed hosts (comma-separated, for production)
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

---

### Generating Keys

#### Django Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use: https://djecrety.ir/

#### Fernet Encryption Key

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

#### Groq API Key

1. Go to https://console.groq.com/keys
2. Click "Create API Key"
3. Copy the key (starts with `gsk_`)

---

### Frontend Environment

The frontend uses environment variables for API configuration.

Create `frontend/.env.local` (optional):

```env
# API URL (defaults to localhost:8000)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/
```

For production:

```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api/
```

---

## Python Setup

### Recommended Python Version

- **Python 3.10+** (tested with 3.11, 3.12)

### Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Verify activation
which python  # Should show path inside venv
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

#### Key Dependencies:

| Package                       | Version | Purpose               |
| ----------------------------- | ------- | --------------------- |
| Django                        | 5.x     | Web framework         |
| djangorestframework           | 3.x     | REST API              |
| djangorestframework-simplejwt | 5.x     | JWT auth              |
| langchain                     | 0.3.x   | LLM framework         |
| langchain-groq                | 0.2.x   | Groq integration      |
| cryptography                  | 44.x    | API key encryption    |
| python-dotenv                 | 1.x     | Environment variables |

---

## Node.js Setup

### Recommended Node Version

- **Node.js 18+** (tested with 18, 20, 22)

### Installing Dependencies

```bash
cd frontend
npm install
```

#### Key Dependencies:

| Package        | Version | Purpose            |
| -------------- | ------- | ------------------ |
| next           | 16.x    | React framework    |
| react          | 19.x    | UI library         |
| axios          | 1.x     | HTTP client        |
| react-markdown | 9.x     | Markdown rendering |

---

## IDE Setup

### VS Code (Recommended)

**Extensions:**

- Python (Microsoft)
- Pylance
- ESLint
- Prettier
- Django

**settings.json:**

```json
{
  "python.defaultInterpreterPath": "./backend/venv/Scripts/python.exe",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### PyCharm

1. Open the `chatbot-react` folder
2. Go to Settings → Project → Python Interpreter
3. Add Interpreter → Existing → Select `backend/venv/Scripts/python.exe`
4. Mark `frontend` as a JavaScript module

---

## Database Setup

### Development (SQLite)

No setup required! Django uses `db.sqlite3` by default.

```bash
cd backend
python manage.py migrate
```

### Production (PostgreSQL)

1. Install PostgreSQL

2. Create database:

```sql
CREATE DATABASE nova_chatbot;
CREATE USER nova_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE nova_chatbot TO nova_user;
```

3. Update `backend/.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nova_chatbot
DB_USER=nova_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

4. Run migrations:

```bash
python manage.py migrate
```

---

## Running the Application

### Development Mode

**Terminal 1 - Backend:**

```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

### Access Points

| Service      | URL                          |
| ------------ | ---------------------------- |
| Frontend     | http://localhost:3000        |
| Backend API  | http://localhost:8000/api/   |
| Django Admin | http://localhost:8000/admin/ |

---

## Common Issues

### Port Already in Use

**Backend (8000):**

```bash
# Find process
netstat -ano | findstr :8000

# Kill it
taskkill /PID <PID> /F
```

**Frontend (3000):**

```bash
# Run on different port
npm run dev -- -p 3001
```

### Virtual Environment Not Activating

Windows PowerShell may block scripts. Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module Not Found Errors

```bash
cd backend
pip install -r requirements.txt --upgrade
```
