from celery import shared_task
from PIL import Image


@shared_task
def resize_post_image(img_path):
    """
    Resize the image uploaded with the post
    to fixed width and proportional height
    """
    img = Image.open(img_path)
    width, height = img.size

    fixed_width = 1170
    width_percent = fixed_width / float(width)
    height_new = int(float(height) * float(width_percent))
    img = img.resize((fixed_width, height_new))
    img.save(img_path)
