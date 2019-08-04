from django.dispatch import Signal

user_joined_society = Signal(providing_args=["user"])
