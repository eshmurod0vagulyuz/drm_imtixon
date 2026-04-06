from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    Validates registration input.
    Fields: username, email, password, confirm_password.
    - Validate that password == confirm_password
    - Validate email is unique
    - create() must hash the password and create the user
    """
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Validates login credentials.
    Fields: email, password.
    - Must authenticate user with email+password
    - Return error if credentials are invalid
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user_obj = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Error")

        user = authenticate(username=user_obj.username, password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        data['user'] = user
        return data


class LogoutSerializer(serializers.Serializer):
    """
    Accepts a refresh token for blacklisting.
    Fields: refresh
    - save() must blacklist the given refresh token
    """
    refresh = serializers.CharField()

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.validated_data['refresh'])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("Invalid token.")


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes user profile for read and update.
    Model: CustomUser
    Fields: id, username, email, first_name, last_name, bio, avatar, website, date_joined
    Read-only: id, email, date_joined
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'bio', 'avatar', 'website', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Validates password reset request.
    Fields: email
    - Must verify email exists in the system
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Validates password reset confirmation.
    Fields: token, new_password, confirm_password
    - Validate token is valid
    - Validate new_password == confirm_password
    """
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

