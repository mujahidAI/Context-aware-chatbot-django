import os
import requests
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from django.conf import settings

load_dotenv()

session_store = {}

def encrypt_api_key(plain_key):
    """Encrypt API key using Fernet"""
    if not plain_key:
        return None
    f = Fernet(settings.ENCRYPTION_KEY.encode())
    return f.encrypt(plain_key.encode()).decode()

def decrypt_api_key(encrypted_key):
    """Decrypt API key"""
    if not encrypted_key:
        return None
    try:
        f = Fernet(settings.ENCRYPTION_KEY.encode())
        return f.decrypt(encrypted_key.encode()).decode()
    except Exception:
        return None

def get_available_models(api_key):
    """Fetch available models from Groq API"""
    if not api_key:
        return []

    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            models = []
            for model in data.get('data', []):
                # Filter for open-source models as requested
                model_id = model['id'].lower()
                # Basic filtering for open source models usually available on Groq
                if any(x in model_id for x in ['llama', 'mixtral', 'gemma', 'deepseek']):
                     models.append({
                        'id': model['id'],
                        'name': model['id'], # Use ID as name for now
                        'context_window': model.get('context_window', 8192) # Default fallback
                    })
            return models
        return []
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


groq_api_key_env = os.getenv("GROQ_API_KEY")


def ask_groq(message, session_id="default_session", language="English", api_key=None, model=None):
    try:
        # Use provided API key or fallback to env
        current_api_key = api_key if api_key else groq_api_key_env

        # Use provided model or fallback to default
        current_model = model if model else "llama-3.3-70b-versatile"

        if not current_api_key:
            return "Error: No API Key provided and no default key available."

        llm = ChatGroq(model=current_model, groq_api_key=current_api_key)
        try:
            with open("system_prompt.txt", "r", encoding="utf-8") as file:
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
        return f"Error: {str(e)}"
