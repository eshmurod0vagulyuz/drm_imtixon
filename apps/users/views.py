from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

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
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User registered successfully.",
            "username": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    """POST /api/v1/users/login/ — Authenticate user and return JWT tokens.
    - permission_classes = [AllowAny]
    - serializer_class = LoginSerializer
    - post() must return access + refresh tokens
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": f"User {user.username} logged in successfully.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    """POST /api/v1/users/logout/ — Blacklist refresh token.
    - permission_classes = [IsAuthenticated]
    - serializer_class = LogoutSerializer
    """
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)


class ProfileAPIView(RetrieveUpdateAPIView):
    """GET/PUT/PATCH /api/v1/users/profile/ — Retrieve or update current user profile.
    - permission_classes = [IsAuthenticated]
    - serializer_class = ProfileSerializer
    - get_object() returns request.user
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordResetRequestAPIView(GenericAPIView):
    """POST /api/v1/users/password-reset/ — Request a password reset email.
    - permission_classes = [AllowAny]
    - serializer_class = PasswordResetRequestSerializer
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password reset link has been sent to your email."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmAPIView(GenericAPIView):
    """POST /api/v1/users/password-reset/confirm/ — Confirm password reset.
    - permission_classes = [AllowAny]
    - serializer_class = PasswordResetConfirmSerializer
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )

