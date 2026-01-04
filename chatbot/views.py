from multiprocessing.connection import answer_challenge
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Chat
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
from django.utils import timezone
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

# ===========================================================================================
# ============= IMPORTANT : READ explanation.ipynb FOR COMPLETE UNDERSTANDING ===============
# ============= IMPORTANT : READ explanation_bot.pdf FOR COMPLETE UNDERSTANDING =============
# ===========================================================================================


session_store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


groq_api_key = os.getenv("GROQ_API_KEY")


def ask_groq(message, session_id="default_session", language="English"):
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
        with open("system_prompt.txt", "r", encoding="utf-8") as file:
            system_prompt = file.read().strip()
        prompt = ChatPromptTemplate.from_messages(
            [
                #                 The MessagesPlaceholder Behavior
                # The MessagesPlaceholder(variable_name="messages") doesn't just insert the current message. It inserts the entire conversation thread for that session, which includes:
                # All previous HumanMessage objects (user inputs)
                # All previous AIMessage objects (AI responses)
                # The current new HumanMessage (user's latest query)
                # This is why the AI can remember earlier parts of the conversation - it literally receives the complete chat history every time, not just the latest message.
                # Memory vs. Context Window
                # The RunnableWithMessageHistory automatically manages this by:
                # Retrieving stored conversation history for the session
                # Appending the new user message
                # Sending everything together to the LLM
                # Storing the AI's response for future conversations
                # This is different from the LLM having "memory" - it's getting the full context each time, which creates the illusion of memory.
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | llm
        with_message_history = RunnableWithMessageHistory(
            chain, get_session_history, input_messages_key="messages"
        )
        config = {"configurable": {"session_id": session_id}}

        response = with_message_history.invoke(
            {"messages": [HumanMessage(content=message)]}, config=config
        )
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"


@login_required(login_url="chatbot:login")
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == "POST":
        message = request.POST.get("message")
        language = request.POST.get("language", "English")
        session_id = request.session.get("chat_session_id")
        if not session_id:
            session_id = (
                f"user_{request.user.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
            )
            request.session["chat_session_id"] = session_id

        # Get response using LangChain with session memory
        response = ask_groq(message, session_id, language)
        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now(),
        )
        chat.save()
        return JsonResponse(
            {"message": message, "response": response, "session_id": session_id}
        )
    return render(request, "chatbot.html", {"chats": chats})


# new


def new_chat_session(request):
    """Start a new chat session"""
    if request.method == "POST":
        # Clear current session
        if "chat_session_id" in request.session:
            del request.session["chat_session_id"]

        return JsonResponse({"message": "New chat session started"})

    return JsonResponse({"error": "Invalid request method"}, status=405)


def clear_session_history(request):
    """Clear the conversation history for current session"""
    session_id = request.session.get("chat_session_id")
    if session_id and session_id in session_store:
        del session_store[session_id]
        return JsonResponse({"message": "Session history cleared"})

    return JsonResponse({"message": "No active session to clear"})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            error_message = "Username and password are required."
            return render(request, "login.html", {"error_message": error_message})
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("chatbot:chatbot")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validate passwords match
        if password1 != password2:
            error_message = "Passwords don't match"
            return render(request, "register.html", {"error_message": error_message})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists"
            return render(request, "register.html", {"error_message": error_message})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            error_message = "Email already exists"
            return render(request, "register.html", {"error_message": error_message})

        try:
            # Create and save user
            user = User.objects.create_user(
                username=username, email=email, password=password1
            )
            user.save()

            # Login the user
            auth.login(request, user)
            return redirect("chatbot:chatbot")

        except Exception as e:
            error_message = f"Error creating account: {str(e)}"
            return render(request, "register.html", {"error_message": error_message})

    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("chatbot:login")


# Custom Password Reset View
class CustomPasswordResetView(PasswordResetView):
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("chatbot:password_reset_done")
    form_class = PasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    success_url = reverse_lazy("chatbot:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"
