from django.contrib.auth import authenticate, password_validation, tokens, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth.password_validation import validate_password

from apps.identity.models import User

# Add Registerserializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    consfirm_password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {
                'required': True
            },
            'last_name': {
                'required': True
            },
            'email': {
                'required': True
            },
        }

    def validate(self, attrs):
        # check passwords match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match."
            })

        # Optional: validate password through using Django's validators
        validate_password(attrs['password'])

        # Check email uniqueness
        if User.objects.filter(email=attrs['email'].lower()).exists():
            raise serializers.ValidationError({
                'email': 'A user with this email already exists.'
            })

        return attrs

    def create(self, validated_data):
        # Remove confirm_password as it's not a model field
        validated_data.pop('confirm_password')

        # Set username to email
        validated_data['username'] = validated_data['email']

        # Create user using create_user
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email = email,
            password = password,
        )

        if user is None:
            raise serializers.ValidationError(
                {
                    "email": "Invalid email or password."
                }
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "detail": "This user account is inactive."
                }
            )
        attrs["user"] = user

        return attrs

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )
        read_only_fields = fields

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        try:
            token = RefreshToken(
                self.validated_data['refresh']
            )
    
            token.blacklist()

        except TokenError:
            raise serializers.ValidationError(
                {
                    "refresh": "Invalid or expired refresh token."
                }
            )

class UpdateCurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            "first_name",
            instance.first_name,
        )

        instance.last_name = validated_data.get(
            "last_name",
            instance.last_name,
        )

        instance.save(
            update_fields=[
                "first_name",
                "last_name",
            ]
        )
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, trim_whitespace=False)

    new_password = serializers.CharField(write_only=True, trim_whitespace=False)

    new_password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = self.context["request"].user

        current_password = attrs.get("current_password")
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")

        # Verify current_password
        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {
                    "current_password": "Current password is incorrect."
                }
            )

        # confirm new passwords match
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {
                    "new_password_confirm": "Passwords do not match."
                }
            )

        # Prevent using the same password
        if current_password == new_password:
            raise serializers.ValidationError(
                {
                    "new_password": "New password must be different from the current password."
                }
            )

        # validate password using Django's configured validators
        password_validation.validate_password(new_password, user)
        return attrs

    def save(self):
        user = self.context["request"].user

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save(
            update_fields=["password"]
        )
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs["email"].lower()

        attrs["email"] = email

        return attrs

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs["uid"]
        token = attrs["token"]
        new_password = attrs["new_password"]
        new_password_confirm = attrs["new_password_confirm"]

        User = get_user_model()

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "uid": [
                        "Invalid password-reset request."
                    ]
                }
            )

        if not tokens.default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {
                    "token": [
                        "Invalid or expired password-reset token."
                    ]
                }
            )

        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {
                    "new_password_confirm": [
                        "Passwords do not match."
                    ]
                }
            )

        password_validation.validate_password(
            new_password,
            user=user,
        )

        attrs["user"] = user

        return attrs
