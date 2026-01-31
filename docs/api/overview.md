# 🔌 API Overview

This document provides an overview of the Nova AI Chatbot REST API architecture.

---

## Base URL

| Environment     | URL                            |
| --------------- | ------------------------------ |
| **Development** | `http://localhost:8000/api/`   |
| **Production**  | `https://your-domain.com/api/` |

---

## Authentication

The API uses **JWT (JSON Web Tokens)** for authentication.

### Token Flow

```
1. Register → POST /api/register/
2. Login    → POST /api/token/ → Returns { access, refresh }
3. Use API  → Authorization: Bearer <access_token>
4. Refresh  → POST /api/token/refresh/ → Returns { access }
```

### Headers

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

### Token Expiry

| Token Type        | Expiry     |
| ----------------- | ---------- |
| **Access Token**  | 15 minutes |
| **Refresh Token** | 7 days     |

---

## Response Format

### Success Response

```json
{
  "id": 1,
  "message": "Hello, how are you?",
  "response": "I'm doing great! How can I help you today?",
  "created_at": "2025-01-31T10:30:00Z"
}
```

### Error Response

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Validation Error

```json
{
  "field_name": ["Error message for this field."]
}
```

---

## API Categories

### 1. Authentication Endpoints

| Method | Endpoint              | Description             |
| ------ | --------------------- | ----------------------- |
| POST   | `/api/register/`      | Create new user account |
| POST   | `/api/token/`         | Get JWT tokens (login)  |
| POST   | `/api/token/refresh/` | Refresh access token    |

### 2. Chat Endpoints

| Method | Endpoint           | Description                   |
| ------ | ------------------ | ----------------------------- |
| GET    | `/api/chat/`       | List all messages for user    |
| POST   | `/api/chat/`       | Send message, get AI response |
| DELETE | `/api/chat/clear/` | Clear chat history            |

### 3. Settings Endpoints

| Method | Endpoint                 | Description              |
| ------ | ------------------------ | ------------------------ |
| GET    | `/api/user-api-key/`     | Get API key status       |
| POST   | `/api/user-api-key/`     | Save/update API key      |
| DELETE | `/api/user-api-key/`     | Remove API key           |
| GET    | `/api/available-models/` | List available AI models |
| POST   | `/api/select-model/`     | Update selected model    |

---

## Rate Limiting

Currently, rate limiting is handled by:

1. **Groq API** - Has its own rate limits based on your API key tier
2. **Django** - No explicit rate limiting (can be added with `django-ratelimit`)

---

## Error Codes

| Status Code | Meaning                              |
| ----------- | ------------------------------------ |
| `200`       | Success                              |
| `201`       | Created successfully                 |
| `400`       | Bad request (validation error)       |
| `401`       | Unauthorized (invalid/missing token) |
| `403`       | Forbidden (not allowed)              |
| `404`       | Not found                            |
| `429`       | Rate limit exceeded                  |
| `500`       | Server error                         |

---

## CORS

The API accepts requests from:

- `http://localhost:3000` (development)
- Your production frontend domain

Configure in `backend/chatbot_project/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend-domain.com",
]
```

---

## See Also

- [API Endpoints Reference](endpoints.md) - Detailed endpoint documentation
- [Architecture](../ARCHITECTURE.md) - System design overview
