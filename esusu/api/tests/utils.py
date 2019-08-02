from api.models import User, Society, Tenure
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import BaseUserSerializer, TenureSerializer
import faker
import arrow
from math import floor

fake = faker.Faker()

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
	society = {
		'name': fake.company(),
		'description': fake.catch_phrase(),
		'maximum_capacity': 10,
		'periodic_amount': 100000,
		'is_searchable': searchable,
		'creator': get_fake_user(),
	}
	return Society.objects.create(**society)

def get_fake_user():
	user = User.objects.filter(is_society_admin=False, society__isnull=True).exclude(email='a.ciroma@confam.com').first()
	if not user:
		create_fake_users(2)
		user = User.objects.filter(is_society_admin=False, society__isnull=True).exclude(email='a.ciroma@confam.com').first()
	return user

def get_unique_email():
	email = None
	while True:
		email = fake.email()
		if User.objects.filter(email=email).first():
			continue
		break
	return email

def create_unique_user():
	email = get_unique_email()
	user = {
		'email': email,
		'first_name': fake.first_name(),
		'last_name': fake.last_name(),
		'password': fake.password(),
	}
	serializer = BaseUserSerializer(data=user)
	serializer.is_valid()
	return serializer.create_user()

def get_unique_user():
	user = User.objects.filter(is_society_admin=False, society__isnull=True).exclude(email='a.ciroma@confam.com').first()
	if not user:
		user = create_unique_user()
	return user

def delete_all_societies():
	Society.objects.all().delete()

def add_user_to_society(society):
	user = get_fake_user()
	user.society = society
	user.save()
	return user

def fill_up_society(society):
	number_of_users_to_add = society.maximum_capacity - society.users.count()
	for _ in range(number_of_users_to_add):
		user = get_unique_user()
		user.society = society
		user.save()

def empty_society(society):
	for user in society.users.all():
		if not user.is_society_admin:
			user.society = None
			user.save()

def create_tenure(society):
	tenure = {
		'start_date': arrow.now('Africa/Lagos').date(),
	}
	serializer = TenureSerializer(data=tenure)
	serializer.society = society
	serializer.is_valid()
	serializer.save()

def get_deadline(tenure):
	start = tenure.tentative_end_date
	stop = tenure.maximum_end_date
	shift = floor((stop - start).days / 2)
	return arrow.get(start).shift(days=shift).date()

