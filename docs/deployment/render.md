# 🚀 Deploy Backend to Render

Deploy your Django backend to Render for free.

---

## Prerequisites

- GitHub account with your code pushed
- [Render account](https://render.com/) (free tier available)
- PostgreSQL addon (free tier: 90 days)

---

## Step 1: Prepare Your Code

### Create `render.yaml` (optional, for Blueprint)

In your project root:

```yaml
services:
  - type: web
    name: nova-chatbot-api
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && gunicorn chatbot_project.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

### Update `requirements.txt`

Add these to `backend/requirements.txt`:

```
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
dj-database-url==2.1.0
```

### Update `settings.py`

Add to `backend/chatbot_project/settings.py`:

```python
import dj_database_url

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database from URL (for Render)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600
    )

# Security for production
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

---

## Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New → Web Service**
3. Connect your GitHub repository
4. Configure:

| Setting            | Value                                       |
| ------------------ | ------------------------------------------- |
| **Name**           | `nova-chatbot-api`                          |
| **Region**         | Closest to your users                       |
| **Branch**         | `main`                                      |
| **Root Directory** | `backend`                                   |
| **Runtime**        | Python 3                                    |
| **Build Command**  | `pip install -r requirements.txt`           |
| **Start Command**  | `gunicorn chatbot_project.wsgi:application` |

---

## Step 3: Add PostgreSQL Database

1. In Render Dashboard, click **New → PostgreSQL**
2. Name it `nova-chatbot-db`
3. Select **Free** plan
4. Create database
5. Copy the **Internal Database URL**

---

## Step 4: Set Environment Variables

In your Web Service, go to **Environment** and add:

| Variable         | Value                           |
| ---------------- | ------------------------------- |
| `DATABASE_URL`   | (paste from PostgreSQL)         |
| `SECRET_KEY`     | (generate a new one)            |
| `GROQ_API_KEY`   | (your Groq API key)             |
| `ENCRYPTION_KEY` | (generate with Fernet)          |
| `DEBUG`          | `False`                         |
| `ALLOWED_HOSTS`  | `nova-chatbot-api.onrender.com` |
| `PYTHON_VERSION` | `3.11.0`                        |

---

## Step 5: Run Migrations

After first deploy, open **Shell** in Render dashboard:

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Step 6: Update Frontend

Update `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=https://nova-chatbot-api.onrender.com/api/
```

---

## Troubleshooting

### Build fails with "gunicorn not found"

Add `gunicorn` to `requirements.txt`

### Static files not loading

Run in Render shell:

```bash
python manage.py collectstatic --no-input
```

### Database connection errors

Check `DATABASE_URL` is set correctly

---

## Cost

| Resource    | Free Tier              |
| ----------- | ---------------------- |
| Web Service | 750 hours/month        |
| PostgreSQL  | 90 days, then $7/month |

> ⚠️ Free tier spins down after 15 min of inactivity
