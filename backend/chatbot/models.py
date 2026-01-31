from django.db import models
from django.contrib.auth.models import User
from django.http import response

# Create your models here.


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # This function returns a string representation of the Chat object,
    # showing the username of the user and their message.
    def __str__(self):
        return f"{self.user.username}: {self.message}"


class UserAPIKey(models.Model):
    """
    Stores encrypted Groq API keys per user along with their selected model preference.
    API keys are encrypted using Fernet symmetric encryption for security.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="api_key_config"
    )
    encrypted_key = models.TextField(help_text="Encrypted Groq API key")
    selected_model = models.CharField(
        max_length=100,
        default="llama-3.3-70b-versatile",
        help_text="The model ID selected by user for chat",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User API Key"
        verbose_name_plural = "User API Keys"

    def __str__(self):
        return f"{self.user.username}'s API Key (Model: {self.selected_model})"
