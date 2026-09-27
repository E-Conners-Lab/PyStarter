from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()


def _run_password_validators(password, user=None):
    """Apply AUTH_PASSWORD_VALIDATORS and re-raise as a DRF error.

    serializers.CharField(min_length=8) does not invoke them, so without this the
    configured common-password and numeric-password rules never run.
    """
    try:
        validate_password(password, user=user)
    except DjangoValidationError as exc:
        raise serializers.ValidationError(list(exc.messages)) from exc
    return password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=1024, trim_whitespace=False)
    email = serializers.EmailField(required=False, default="")

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def validate_password(self, value):
        # User is unsaved at this point; pass the attrs we have so the
        # similarity validator can compare against the username.
        candidate = User(
            username=self.initial_data.get("username", ""),
            email=self.initial_data.get("email", "") or "",
        )
        return _run_password_validators(value, user=candidate)

    def create(self, validated_data):
        email = validated_data.get("email", "")
        if not email:
            # Generate a unique placeholder when no email is provided,
            # since User.email has unique=True
            email = f"{validated_data['username']}@placeholder.pystarter.dev"
        user = User.objects.create_user(
            username=validated_data["username"],
            email=email,
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    current_belt = serializers.CharField(read_only=True)
    current_belt_display = serializers.CharField(read_only=True)
    next_belt_xp = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "bio",
            "total_xp",
            "current_belt",
            "current_belt_display",
            "next_belt_xp",
            "current_streak",
            "longest_streak",
            "last_activity_date",
            "created_at",
        )
        read_only_fields = ("total_xp", "current_streak", "longest_streak", "created_at")


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, max_length=1024, trim_whitespace=False)

    def validate_new_password(self, value):
        return _run_password_validators(value)


class UserProgressSummarySerializer(serializers.Serializer):
    """Summary of a user's overall progress."""

    total_xp = serializers.IntegerField()
    current_belt = serializers.CharField()
    modules_completed = serializers.IntegerField()
    modules_total = serializers.IntegerField()
    exercises_completed = serializers.IntegerField()
    exercises_total = serializers.IntegerField()
    current_streak = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=1024, trim_whitespace=False, write_only=True)
