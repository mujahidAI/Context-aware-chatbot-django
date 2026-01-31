from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, ChatSerializer, UserAPIKeySerializer, AvailableModelsSerializer
from .models import Chat, UserAPIKey
from .services import ask_groq, get_available_models, decrypt_api_key
from django.utils import timezone


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class ChatListCreateView(generics.ListCreateAPIView):
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
            # Default to a persistent session for the user if none provided
            session_id = f"user_{request.user.id}"

        # Fetch user's API key and model
        api_key = None
        model = None
        try:
            user_api_key = UserAPIKey.objects.get(user=request.user)
            api_key = decrypt_api_key(user_api_key.encrypted_key)
            model = user_api_key.selected_model
        except UserAPIKey.DoesNotExist:
            pass

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
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # In a real stateless API, clearing "session" is just the client discarding the ID.
        # But here we have server-side memory (session_store).
        # We need the session_id to clear it.
        session_id = request.data.get("session_id")
        if not session_id:
            session_id = f"user_{request.user.id}"

        from .services import session_store

        if session_id in session_store:
            del session_store[session_id]
            return Response({"message": "Session history cleared"})
        return Response({"message": "No active session to clear"})


class UserAPIKeyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user_api_key = UserAPIKey.objects.get(user=request.user)
            serializer = UserAPIKeySerializer(user_api_key)
            return Response(serializer.data)
        except UserAPIKey.DoesNotExist:
            return Response({})

    def post(self, request):
        serializer = UserAPIKeySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user_api_key = UserAPIKey.objects.get(user=request.user)
            user_api_key.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserAPIKey.DoesNotExist:
            return Response({"error": "No API key found"}, status=status.HTTP_404_NOT_FOUND)


class AvailableModelsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user_api_key = UserAPIKey.objects.get(user=request.user)
            api_key = decrypt_api_key(user_api_key.encrypted_key)
            if not api_key:
                return Response({"error": "Invalid API key"}, status=status.HTTP_400_BAD_REQUEST)

            models = get_available_models(api_key)
            serializer = AvailableModelsSerializer(models, many=True)
            return Response(serializer.data)
        except UserAPIKey.DoesNotExist:
             return Response({"error": "No API key found. Please save your Groq API key first."}, status=status.HTTP_404_NOT_FOUND)
