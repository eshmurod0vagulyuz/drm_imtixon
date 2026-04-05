from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    Validates registration input.
    Fields: username, email, password, confirm_password.
    - Validate that password == confirm_password
    - Validate email is unique
    - create() must hash the password and create the user
    """
    pass


class LoginSerializer(serializers.Serializer):
    """
    Validates login credentials.
    Fields: email, password.
    - Must authenticate user with email+password
    - Return error if credentials are invalid
    """
    pass


class LogoutSerializer(serializers.Serializer):
    """
    Accepts a refresh token for blacklisting.
    Fields: refresh
    - save() must blacklist the given refresh token
    """
    pass


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes user profile for read and update.
    Model: CustomUser
    Fields: id, username, email, first_name, last_name, bio, avatar, website, date_joined
    Read-only: id, email, date_joined
    """
    pass


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Validates password reset request.
    Fields: email
    - Must verify email exists in the system
    """
    pass


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Validates password reset confirmation.
    Fields: token, new_password, confirm_password
    - Validate token is valid
    - Validate new_password == confirm_password
    """
    pass

