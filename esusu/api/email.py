from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_invite(subject, from_email, to, **email_values):
    html_content = render_to_string('invite.html', email_values)
    text_content = strip_tags(html_content)
    send_mail(
        subject, text_content, from_email, [to],
        fail_silently=False,
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
        html_message=html_content,
    )
