from ..models import User
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import BaseUserSerializer


def create_test_user():
    user = {
        'email': 'a.ciroma@confam.com',
        'first_name': 'Adamu',
        'last_name': 'Ciroma',
        'password': 'testpassword',
    }
    serializer = BaseUserSerializer(data=user)
    serializer.is_valid()
    return serializer.create_user()

def get_test_user():
    user = User.objects.filter(email='a.ciroma@confam.com').first()
    if not user:
        user = create_test_user()
    return user

def get_auth_token():
    user = get_test_user()
    token = RefreshToken.for_user(user)
    return token
