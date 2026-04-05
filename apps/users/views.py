from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


class RegisterAPIView(CreateAPIView):
    """POST /api/v1/users/register/ — Register a new user.
    - permission_classes = [AllowAny]
    - serializer_class = RegisterSerializer
    """
    pass


class LoginAPIView(GenericAPIView):
    """POST /api/v1/users/login/ — Authenticate user and return JWT tokens.
    - permission_classes = [AllowAny]
    - serializer_class = LoginSerializer
    - post() must return access + refresh tokens
    """
    pass


class LogoutAPIView(GenericAPIView):
    """POST /api/v1/users/logout/ — Blacklist refresh token.
    - permission_classes = [IsAuthenticated]
    - serializer_class = LogoutSerializer
    """
    pass


class ProfileAPIView(RetrieveUpdateAPIView):
    """GET/PUT/PATCH /api/v1/users/profile/ — Retrieve or update current user profile.
    - permission_classes = [IsAuthenticated]
    - serializer_class = ProfileSerializer
    - get_object() returns request.user
    """
    pass


class PasswordResetRequestAPIView(GenericAPIView):
    """POST /api/v1/users/password-reset/ — Request a password reset email.
    - permission_classes = [AllowAny]
    - serializer_class = PasswordResetRequestSerializer
    """
    pass


class PasswordResetConfirmAPIView(GenericAPIView):
    """POST /api/v1/users/password-reset/confirm/ — Confirm password reset.
    - permission_classes = [AllowAny]
    - serializer_class = PasswordResetConfirmSerializer
    """
    pass

