from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chat, UserAPIKey
from .services import encrypt_api_key


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
    api_key = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserAPIKey
        fields = ('api_key', 'selected_model', 'updated_at')
        read_only_fields = ('updated_at',)

    def create(self, validated_data):
        user = self.context['request'].user
        api_key = validated_data.pop('api_key', None)
        selected_model = validated_data.get('selected_model', 'llama-3.3-70b-versatile')

        defaults = {'selected_model': selected_model}
        if api_key:
            defaults['encrypted_key'] = encrypt_api_key(api_key)

        user_api_key, created = UserAPIKey.objects.update_or_create(
            user=user,
            defaults=defaults
        )
        return user_api_key

    def update(self, instance, validated_data):
        if 'api_key' in validated_data:
            instance.encrypted_key = encrypt_api_key(validated_data.pop('api_key'))
        instance.selected_model = validated_data.get('selected_model', instance.selected_model)
        instance.save()
        return instance


class AvailableModelsSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    context_window = serializers.IntegerField()
