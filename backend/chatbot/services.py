import os
import requests
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

session_store = {}

# Default API key from environment (fallback)
default_groq_api_key = os.getenv("GROQ_API_KEY")

# Encryption key for securing user API keys
encryption_key = os.getenv("ENCRYPTION_KEY")


def get_fernet():
    """Get Fernet instance for encryption/decryption."""
    if not encryption_key:
        raise ValueError("ENCRYPTION_KEY not found in environment variables")
    return Fernet(encryption_key.encode())


def encrypt_api_key(plain_key: str) -> str:
    """
    Encrypt an API key using Fernet symmetric encryption.

    Args:
        plain_key: The plain text API key to encrypt

    Returns:
        The encrypted API key as a string
    """
    fernet = get_fernet()
    encrypted = fernet.encrypt(plain_key.encode())
    return encrypted.decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """
    Decrypt an encrypted API key.

    Args:
        encrypted_key: The encrypted API key string

    Returns:
        The decrypted plain text API key
    """
    fernet = get_fernet()
    decrypted = fernet.decrypt(encrypted_key.encode())
    return decrypted.decode()


def validate_groq_api_key(api_key: str) -> dict:
    """
    Validate a Groq API key by making a test request to list models.

    Args:
        api_key: The Groq API key to validate

    Returns:
        dict with 'valid' boolean and 'error' message if invalid
    """
    try:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        if response.status_code == 200:
            return {"valid": True, "error": None}
        elif response.status_code == 401:
            return {"valid": False, "error": "Invalid API key"}
        else:
            return {"valid": False, "error": f"API error: {response.status_code}"}
    except requests.RequestException as e:
        return {"valid": False, "error": f"Connection error: {str(e)}"}


def get_available_models(api_key: str) -> list:
    """
    Fetch available models from Groq API using the provided API key.
    Filters to only include open-source chat models.

    Args:
        api_key: The Groq API key

    Returns:
        List of available model dictionaries with id, name, and context_window
    """
    try:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )

        if response.status_code != 200:
            return []

        data = response.json()
        models = data.get("data", [])

        # Filter for open-source chat models (exclude whisper, vision-only, etc.)
        open_source_patterns = [
            "llama",
            "mixtral",
            "mistral",
            "gemma",
            "qwen",
            "deepseek",
            "gpt-oss",
        ]

        filtered_models = []
        for model in models:
            model_id = model.get("id", "").lower()
            # Check if it's an open-source model
            if any(pattern in model_id for pattern in open_source_patterns):
                # Exclude audio/whisper models
                if "whisper" not in model_id and "audio" not in model_id:
                    filtered_models.append(
                        {
                            "id": model.get("id"),
                            "name": model.get("id").replace("-", " ").title(),
                            "context_window": model.get("context_window", 8192),
                            "owned_by": model.get("owned_by", "Unknown"),
                        }
                    )

        # Sort by model name
        filtered_models.sort(key=lambda x: x["id"])
        return filtered_models

    except requests.RequestException:
        return []


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get or create a chat message history for a session."""
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


def ask_groq(
    message: str,
    session_id: str = "default_session",
    language: str = "English",
    api_key: str = None,
    model: str = None,
) -> str:
    """
    Send a message to Groq LLM and get a context-aware response.

    Args:
        message: The user's message
        session_id: Unique session identifier for conversation memory
        language: Response language (currently unused, for future)
        api_key: Optional custom API key (uses default if not provided)
        model: Optional model ID (uses default if not provided)

    Returns:
        The AI's response as a string
    """
    try:
        # Use provided API key or fall back to default
        active_api_key = api_key or default_groq_api_key
        active_model = model or "llama-3.3-70b-versatile"

        if not active_api_key:
            return "Error: No API key configured. Please add your Groq API key in the sidebar."

        llm = ChatGroq(model=active_model, groq_api_key=active_api_key)

        # Get the path to system_prompt.txt relative to this file's location
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(base_dir, "system_prompt.txt")

        try:
            with open(prompt_path, "r", encoding="utf-8") as file:
                system_prompt = file.read().strip()
        except FileNotFoundError:
            system_prompt = "You are a helpful AI assistant."

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | llm
        with_message_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="messages",
        )
        config = {"configurable": {"session_id": session_id}}

        response = with_message_history.invoke(
            {"messages": [HumanMessage(content=message)]}, config=config
        )
        return response.content

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            return "Error: Invalid API key. Please check your Groq API key."
        elif "rate" in error_msg.lower():
            return "Error: Rate limit exceeded. Please wait a moment and try again."
        return f"Error: {error_msg}"
