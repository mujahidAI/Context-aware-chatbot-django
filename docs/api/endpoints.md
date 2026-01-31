# 📡 API Endpoints Reference

Complete reference for all API endpoints in the Nova AI Chatbot.

---

## Authentication

### Register User

Create a new user account.

```http
POST /api/register/
```

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**

```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "tokens": {
    "access": "eyJhbGciO...",
    "refresh": "eyJhbGciO..."
  }
}
```

**Errors:**
| Status | Reason |
|--------|--------|
| 400 | Username already exists |
| 400 | Password too weak |

---

### Login (Get Tokens)

Authenticate and receive JWT tokens.

```http
POST /api/token/
```

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (200 OK):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Refresh Token

Get a new access token using refresh token.

```http
POST /api/token/refresh/
```

**Request Body:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## Chat

> ⚠️ All chat endpoints require authentication.

### Get Chat History

Retrieve all messages for the authenticated user.

```http
GET /api/chat/
Authorization: Bearer <access_token>
```

**Response (200 OK):**

```json
[
  {
    "id": 1,
    "message": "What is Python?",
    "response": "Python is a high-level programming language...",
    "created_at": "2025-01-31T10:30:00Z"
  },
  {
    "id": 2,
    "message": "How do I install it?",
    "response": "You can install Python from python.org...",
    "created_at": "2025-01-31T10:31:00Z"
  }
]
```

---

### Send Message

Send a message and receive an AI response.

```http
POST /api/chat/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "message": "Explain machine learning in simple terms"
}
```

**Response (201 Created):**

```json
{
  "id": 3,
  "message": "Explain machine learning in simple terms",
  "response": "Machine learning is like teaching a computer by example...",
  "created_at": "2025-01-31T10:35:00Z"
}
```

**Possible Response Errors:**
| Status | Reason |
|--------|--------|
| 400 | Empty message |
| 401 | Not authenticated |
| 500 | AI service error (check response message) |

---

### Clear Chat History

Delete all chat messages for the authenticated user.

```http
DELETE /api/chat/clear/
Authorization: Bearer <access_token>
```

**Response (200 OK):**

```json
{
  "message": "Chat history cleared successfully"
}
```

---

## User Settings

> ⚠️ All settings endpoints require authentication.

### Get API Key Status

Check if user has configured an API key.

```http
GET /api/user-api-key/
Authorization: Bearer <access_token>
```

**Response (200 OK) - Key exists:**

```json
{
  "has_key": true,
  "key_preview": "gsk_...X4h",
  "selected_model": "llama-3.3-70b-versatile",
  "updated_at": "2025-01-31T10:00:00Z"
}
```

**Response (200 OK) - No key:**

```json
{
  "has_key": false,
  "selected_model": "llama-3.3-70b-versatile",
  "key_preview": null
}
```

---

### Save/Update API Key

Save or update the user's Groq API key.

```http
POST /api/user-api-key/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "api_key": "gsk_xxxxxxxxxxxxxxxxxxxx",
  "selected_model": "llama-3.3-70b-versatile"
}
```

**Response (200 OK):**

```json
{
  "has_key": true,
  "key_preview": "gsk_...xxx",
  "selected_model": "llama-3.3-70b-versatile",
  "updated_at": "2025-01-31T10:00:00Z"
}
```

**Errors:**
| Status | Reason |
|--------|--------|
| 400 | Invalid API key (validation failed) |
| 400 | API key too short |

---

### Delete API Key

Remove the user's stored API key.

```http
DELETE /api/user-api-key/
Authorization: Bearer <access_token>
```

**Response (200 OK):**

```json
{
  "message": "API key deleted successfully"
}
```

---

### Get Available Models

Fetch list of available AI models from Groq.

```http
GET /api/available-models/
Authorization: Bearer <access_token>
```

**Response (200 OK):**

```json
{
  "models": [
    {
      "id": "llama-3.3-70b-versatile",
      "name": "Llama 3.3 70b Versatile",
      "context_window": 131072,
      "owned_by": "Meta"
    },
    {
      "id": "mixtral-8x7b-32768",
      "name": "Mixtral 8x7b 32768",
      "context_window": 32768,
      "owned_by": "Mistral AI"
    },
    {
      "id": "gemma2-9b-it",
      "name": "Gemma2 9b It",
      "context_window": 8192,
      "owned_by": "Google"
    }
  ]
}
```

> **Note:** Requires user to have a valid API key configured.

---

### Update Selected Model

Change the user's preferred AI model.

```http
POST /api/select-model/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "selected_model": "mixtral-8x7b-32768"
}
```

**Response (200 OK):**

```json
{
  "message": "Model updated successfully",
  "selected_model": "mixtral-8x7b-32768"
}
```

---

## Testing with cURL

### Login and get token:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"pass123"}'
```

### Send a chat message:

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello, who are you?"}'
```

### Get available models:

```bash
curl -X GET http://localhost:8000/api/available-models/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
