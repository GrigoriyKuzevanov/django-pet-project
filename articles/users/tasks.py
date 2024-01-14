from django.core.mail import send_mail
from celery import shared_task
import os

@shared_task
def send_user_registration_mail_task(email_address, message):

    send_mail(
        "DJ-Blog registration",
        f"{message}\n\nThank you!",
        os.getenv("EMAIL_HOST_USER"),
        [email_address],
        fail_silently=False,
    )
