from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, ChatSerializer
from .models import Chat
from .services import ask_groq
from django.utils import timezone

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by('created_at')

    def create(self, request, *args, **kwargs):
        message = request.data.get('message')
        session_id = request.data.get('session_id')

        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not session_id:
             # Default to a persistent session for the user if none provided
            session_id = f"user_{request.user.id}"

        response_text = ask_groq(message, session_id)

        chat = Chat.objects.create(
            user=request.user,
            message=message,
            response=response_text,
            created_at=timezone.now()
        )

        serializer = self.get_serializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClearSessionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # In a real stateless API, clearing "session" is just the client discarding the ID.
        # But here we have server-side memory (session_store).
        # We need the session_id to clear it.
        session_id = request.data.get('session_id')
        if not session_id:
            session_id = f"user_{request.user.id}"

        from .services import session_store
        if session_id in session_store:
            del session_store[session_id]
            return Response({"message": "Session history cleared"})
        return Response({"message": "No active session to clear"})
