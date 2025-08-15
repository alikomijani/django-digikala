from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.utils import verify_otp
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering new users."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "password",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 6},
            "email": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        """Use create_user to ensure password hashing."""
        return User.objects.create_user(**validated_data)  # type: ignore

    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            {"detail": "Updating is not allowed in registration serializer."}
        )


class UserInfoSerializer(serializers.ModelSerializer):
    """Serializer for displaying user info."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile",
            "last_login",
            "date_joined",
        )
        read_only_fields = ("last_login", "date_joined")


class UserChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""

    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_password(self, value):
        """Check that the old password is correct."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        """Add extra password strength checks if needed."""
        # Example: length check already in min_length, but you could add regex checks here
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class OTPRequestSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)


class OTPLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)
    session_id = serializers.CharField(max_length=36)

    def validate(self, attrs):
        mobile = attrs.get("mobile")
        code = attrs.get("code")
        session_id = attrs.get("session_id")

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError({"mobile": "User not found."})

        otp = verify_otp(user, code, session_id)  # Returns OTP instance or raises error

        # Save user and otp in validated_data to avoid extra queries
        attrs["user"] = user
        attrs["otp"] = otp
        return attrs

    def save(self, **kwargs):
        """Mark OTP as used and return JWT token."""
        otp = self.validated_data["otp"]
        user = self.validated_data["user"]

        # Mark OTP as used
        otp.is_used = True
        otp.save(update_fields=["is_used"])

        # Generate token
        refresh = RefreshToken.for_user(user)
        return {"user": user, "access": refresh.access_token, "refresh": str(refresh)}
