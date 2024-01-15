from django.core.mail import send_mail
from celery import shared_task
import os

@shared_task
def send_mail_to_user_task(email_address, message, subject):
    send_mail(
        subject,
        f"{message}\n\nThank you!",
        os.getenv("EMAIL_HOST_USER"),
        [email_address],
        fail_silently=False,
    )
