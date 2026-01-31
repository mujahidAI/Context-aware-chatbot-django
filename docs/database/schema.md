# 🗄️ Database Schema

This document describes the database models used in the Nova AI Chatbot.

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          Django User                             │
│  (Built-in auth_user table)                                      │
├─────────────────────────────────────────────────────────────────┤
│  id          │ INTEGER    │ Primary Key                          │
│  username    │ VARCHAR    │ Unique                               │
│  email       │ VARCHAR    │                                      │
│  password    │ VARCHAR    │ Hashed                               │
│  ...         │            │ (other Django auth fields)           │
└─────────────────────────────────────────────────────────────────┘
          │                              │
          │ 1:N                          │ 1:1
          ▼                              ▼
┌─────────────────────────┐    ┌────────────────────────────────┐
│         Chat            │    │         UserAPIKey             │
├─────────────────────────┤    ├────────────────────────────────┤
│  id         │ INTEGER   │    │  id             │ INTEGER      │
│  user_id    │ FK(User)  │    │  user_id        │ FK(User) UQ  │
│  message    │ TEXT      │    │  encrypted_key  │ TEXT         │
│  response   │ TEXT      │    │  selected_model │ VARCHAR(100) │
│  created_at │ DATETIME  │    │  created_at     │ DATETIME     │
└─────────────────────────┘    │  updated_at     │ DATETIME     │
                               └────────────────────────────────┘
```

---

## Models

### User (Django Built-in)

The standard Django `User` model from `django.contrib.auth.models`.

| Field         | Type           | Description            |
| ------------- | -------------- | ---------------------- |
| `id`          | AutoField      | Primary key            |
| `username`    | CharField(150) | Unique username        |
| `email`       | EmailField     | User's email address   |
| `password`    | CharField      | Hashed password        |
| `is_active`   | BooleanField   | Account active status  |
| `date_joined` | DateTimeField  | Registration timestamp |

---

### Chat

Stores chat messages and AI responses.

**Location:** `backend/chatbot/models.py`

```python
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

| Field        | Type             | Description           |
| ------------ | ---------------- | --------------------- |
| `id`         | AutoField        | Primary key           |
| `user`       | ForeignKey(User) | Owner of the message  |
| `message`    | TextField        | User's input message  |
| `response`   | TextField        | AI's response         |
| `created_at` | DateTimeField    | When message was sent |

**Relationships:**

- `user` → Many-to-One with User (a user can have many chats)

**Indexes:**

- Primary key on `id`
- Foreign key index on `user_id`

---

### UserAPIKey

Stores encrypted API keys and model preferences.

**Location:** `backend/chatbot/models.py`

```python
class UserAPIKey(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='api_key_config'
    )
    encrypted_key = models.TextField(
        help_text="Encrypted Groq API key"
    )
    selected_model = models.CharField(
        max_length=100,
        default='llama-3.3-70b-versatile',
        help_text="The model ID selected by user for chat"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

| Field            | Type                | Description               |
| ---------------- | ------------------- | ------------------------- |
| `id`             | AutoField           | Primary key               |
| `user`           | OneToOneField(User) | Owner (unique per user)   |
| `encrypted_key`  | TextField           | Fernet-encrypted API key  |
| `selected_model` | CharField(100)      | Selected AI model ID      |
| `created_at`     | DateTimeField       | When key was first saved  |
| `updated_at`     | DateTimeField       | When key was last updated |

**Relationships:**

- `user` → One-to-One with User (each user has one key config)

**Security:**

- API keys are encrypted using Fernet (AES-256)
- Never stored in plain text
- Decrypted only when needed for API calls

---

## Migrations

### Initial Migration (0001)

- Creates `Chat` model

### API Key Migration (0002)

- Creates `UserAPIKey` model

**Running Migrations:**

```bash
cd backend
python manage.py migrate
```

**Creating New Migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Database Backends

| Environment     | Database   | Configuration                 |
| --------------- | ---------- | ----------------------------- |
| **Development** | SQLite     | `db.sqlite3` file             |
| **Production**  | PostgreSQL | Set via environment variables |

**Production Configuration:**

Set in `backend/.env`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nova_chatbot
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432
```

---

## Common Queries

### Get all chats for a user:

```python
from chatbot.models import Chat
chats = Chat.objects.filter(user=request.user).order_by('created_at')
```

### Get user's API key config:

```python
from chatbot.models import UserAPIKey
config = UserAPIKey.objects.get(user=request.user)
```

### Check if user has API key:

```python
has_key = UserAPIKey.objects.filter(user=request.user).exists()
```

### Delete all chats for a user:

```python
Chat.objects.filter(user=request.user).delete()
```
