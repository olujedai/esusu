from rest_framework import serializers, status
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'is_staff',
            'is_society_admin',
            'is_superuser',
            'is_active',
            'date_joined',
        ]

    def create_user(self):
        return User.objects.create_user(**self.validated_data)

    def create_superuser(self):
        return User.objects.create_superuser(**self.validated_data)


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_email(self, value):
        email = User.objects.normalize_email(value)
        user = User.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError(
                "This email address already exists.", 
            )
        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match.")

        return data
