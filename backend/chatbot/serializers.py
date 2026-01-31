from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chat, UserAPIKey
from .services import encrypt_api_key, validate_groq_api_key


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def validate_username(self, value):
        """Validate username uniqueness"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        """Validate password using Django's password validators"""
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError as DjangoValidationError

        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        """Create user with validated data"""
        try:
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("id", "message", "response", "created_at")
        read_only_fields = ("response", "created_at")


class UserAPIKeySerializer(serializers.ModelSerializer):
    """
    Serializer for managing user API keys.
    Accepts plain text API key on write, stores encrypted version.
    """

    api_key = serializers.CharField(write_only=True, min_length=10)
    has_key = serializers.SerializerMethodField()
    key_preview = serializers.SerializerMethodField()

    class Meta:
        model = UserAPIKey
        fields = ("api_key", "selected_model", "has_key", "key_preview", "updated_at")
        read_only_fields = ("has_key", "key_preview", "updated_at")

    def get_has_key(self, obj):
        """Check if user has an API key configured."""
        return bool(obj.encrypted_key)

    def get_key_preview(self, obj):
        """Return masked preview of the API key (first 4 and last 4 chars)."""
        if not obj.encrypted_key:
            return None
        from .services import decrypt_api_key

        try:
            decrypted = decrypt_api_key(obj.encrypted_key)
            if len(decrypted) > 8:
                return f"{decrypted[:4]}...{decrypted[-4:]}"
            return "****"
        except Exception:
            return "****"

    def validate_api_key(self, value):
        """Validate the API key by testing it with Groq API."""
        result = validate_groq_api_key(value)
        if not result["valid"]:
            raise serializers.ValidationError(result["error"])
        return value

    def create(self, validated_data):
        """Create a new API key record for the user."""
        user = self.context["request"].user
        api_key = validated_data.pop("api_key")
        encrypted = encrypt_api_key(api_key)

        return UserAPIKey.objects.create(
            user=user,
            encrypted_key=encrypted,
            selected_model=validated_data.get(
                "selected_model", "llama-3.3-70b-versatile"
            ),
        )

    def update(self, instance, validated_data):
        """Update existing API key record."""
        if "api_key" in validated_data:
            api_key = validated_data.pop("api_key")
            instance.encrypted_key = encrypt_api_key(api_key)

        instance.selected_model = validated_data.get(
            "selected_model", instance.selected_model
        )
        instance.save()
        return instance


class AvailableModelSerializer(serializers.Serializer):
    """Serializer for available Groq models."""

    id = serializers.CharField()
    name = serializers.CharField()
    context_window = serializers.IntegerField()
    owned_by = serializers.CharField()
