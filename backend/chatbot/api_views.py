from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import (
    UserSerializer,
    ChatSerializer,
    UserAPIKeySerializer,
    AvailableModelSerializer,
)
from .models import Chat, UserAPIKey
from .services import ask_groq, get_available_models, decrypt_api_key
from django.utils import timezone


class RegisterView(generics.CreateAPIView):
    """Handle user registration."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class ChatListCreateView(generics.ListCreateAPIView):
    """
    List user's chat history and create new chat messages.
    Uses user's custom API key and model if configured.
    """

    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by("created_at")

    def create(self, request, *args, **kwargs):
        message = request.data.get("message")
        session_id = request.data.get("session_id")

        if not message:
            return Response(
                {"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not session_id:
            session_id = f"user_{request.user.id}"

        # Get user's custom API key and model if configured
        api_key = None
        model = None
        try:
            user_api_config = UserAPIKey.objects.get(user=request.user)
            if user_api_config.encrypted_key:
                api_key = decrypt_api_key(user_api_config.encrypted_key)
                model = user_api_config.selected_model
        except UserAPIKey.DoesNotExist:
            pass  # Will use default API key from environment

        response_text = ask_groq(message, session_id, api_key=api_key, model=model)

        chat = Chat.objects.create(
            user=request.user,
            message=message,
            response=response_text,
            created_at=timezone.now(),
        )

        serializer = self.get_serializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClearSessionView(APIView):
    """Clear the conversation history for the current session."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        session_id = request.data.get("session_id")
        if not session_id:
            session_id = f"user_{request.user.id}"

        from .services import session_store

        if session_id in session_store:
            del session_store[session_id]
            return Response({"message": "Session history cleared"})
        return Response({"message": "No active session to clear"})


class UserAPIKeyView(APIView):
    """
    Manage user's Groq API key configuration.
    GET: Check if user has API key and get selected model
    POST: Save/update API key and model selection
    DELETE: Remove user's API key
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Get user's API key status and selected model."""
        try:
            api_config = UserAPIKey.objects.get(user=request.user)
            serializer = UserAPIKeySerializer(api_config)
            return Response(serializer.data)
        except UserAPIKey.DoesNotExist:
            return Response(
                {
                    "has_key": False,
                    "selected_model": "llama-3.3-70b-versatile",
                    "key_preview": None,
                }
            )

    def post(self, request):
        """Save or update user's API key."""
        try:
            api_config = UserAPIKey.objects.get(user=request.user)
            serializer = UserAPIKeySerializer(
                api_config,
                data=request.data,
                context={"request": request},
                partial=True,
            )
        except UserAPIKey.DoesNotExist:
            serializer = UserAPIKeySerializer(
                data=request.data, context={"request": request}
            )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "API key saved successfully", **serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Remove user's API key."""
        try:
            api_config = UserAPIKey.objects.get(user=request.user)
            api_config.delete()
            return Response({"message": "API key removed"})
        except UserAPIKey.DoesNotExist:
            return Response(
                {"error": "No API key configured"}, status=status.HTTP_404_NOT_FOUND
            )


class UpdateSelectedModelView(APIView):
    """Update only the selected model without changing the API key."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        model = request.data.get("selected_model")
        if not model:
            return Response(
                {"error": "selected_model is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            api_config = UserAPIKey.objects.get(user=request.user)
            api_config.selected_model = model
            api_config.save()
            return Response({"message": "Model updated", "selected_model": model})
        except UserAPIKey.DoesNotExist:
            return Response(
                {"error": "Please save your API key first"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AvailableModelsView(APIView):
    """Fetch available models from Groq using user's API key."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Get list of available open-source models."""
        try:
            api_config = UserAPIKey.objects.get(user=request.user)
            if not api_config.encrypted_key:
                return Response(
                    {"error": "No API key configured"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            api_key = decrypt_api_key(api_config.encrypted_key)
            models = get_available_models(api_key)

            if not models:
                return Response(
                    {"error": "Could not fetch models. Please check your API key."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = AvailableModelSerializer(models, many=True)
            return Response(
                {"models": serializer.data, "selected_model": api_config.selected_model}
            )

        except UserAPIKey.DoesNotExist:
            return Response(
                {"error": "Please save your API key first"},
                status=status.HTTP_400_BAD_REQUEST,
            )
