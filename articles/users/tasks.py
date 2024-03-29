import os

from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from PIL import Image
from time import sleep


@shared_task
def send_mail_to_user_task(email_address, message, subject):
    send_mail(
        subject,
        f"{message}\n\nThank you!",
        os.getenv("EMAIL_HOST_USER"),
        [email_address],
        fail_silently=False,
    )


@shared_task
def resize_user_avatar(img_path):
    """
    Resize the image uploaded by user.
    First: proportional resize to height 240
    Second: crop width to 240
    """
    img = Image.open(img_path)
    width, height = img.size

    fixed_height = 240
    height_percent = fixed_height / float(height)
    width_new = int(float(width) * float(height_percent))
    img = img.resize((width_new, fixed_height))

    crop = int((width_new - fixed_height) / 2)
    new_img = img.crop((crop, 0, width_new - crop, fixed_height))

    new_img.save(img_path)

@shared_task
def send_mail_to_user_pass_reset_task(
    subject,
    body,
    from_email,
    to_email,
    html_email=None,
    ):
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email is not None:
             email_message.attach_alternative(html_email, "text/html")
        email_message.send()
