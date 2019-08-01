from api.models import User, Society
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import BaseUserSerializer
import faker


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

def get_auth_token(user=None):
    if not user:
        user = get_test_user()
    token = RefreshToken.for_user(user)
    return token

def create_fake_users(count):
    fake = faker.Faker()
    for _ in range(count):
        user = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': fake.password(),
        }
        serializer = BaseUserSerializer(data=user)
        valid = serializer.is_valid()
        if not valid:
            count += 1
            continue
        serializer.create_user()

def create_fake_society(searchable=True):
    fake = faker.Faker()
    society = {
        'name': fake.company(),
        'description': fake.catch_phrase(),
        'maximum_capacity': int(fake.numerify()),
        'periodic_amount': 100000,
        'is_searchable': searchable,
        'creator': get_fake_user(),
    }
    return Society.objects.create(**society)

def get_fake_user():
    user = User.objects.exclude(email='a.ciroma@confam.com', is_society_admin=False).first()
    if not user:
        create_fake_users(2)
        user = User.objects.exclude(email='a.ciroma@confam.com', is_society_admin=False).first()
    return user

def delete_all_societies():
    Society.objects.all().delete()
