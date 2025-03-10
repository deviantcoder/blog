import os
from io import BytesIO

from django.core.files import File
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.template.loader import render_to_string

from django.conf import settings

from PIL import Image


def compress_image(file):
    """
    Compresses an image file by converting it to JPEG format and reducing its quality.
    """

    try:
        with Image.open(file) as image:
            if image.mode in ('P', 'RGBA'):
                image = image.convert('RGB')

            image_io = BytesIO()
            name = os.path.splitext(file.name)[0] + '.jpg'
            image.save(image_io, format='JPEG', quality=50, optimize=True)

            return File(image_io, name=name)

    except Exception as e:
        pass # logging will be here


def validate_file_size(max_size_mb: int = 10):
    """
    Returns a validator function that checks if a file's size exceeds the specified maximum size.
    Args:
        max_size_mb (int): The maximum file size in megabytes. Defaults to 10 MB.
    Returns:
        function: A validator function that takes a file object and raises a ValidationError if the file size exceeds the specified maximum size.
    """
    
    def _validate(file):
        max_size_bytes = max_size_mb * 1024 * 1024
        if file.size > max_size_bytes:
            raise ValidationError(f'File size cannot exceed {max_size_mb} MB. Current file size: {file.size}')

    return _validate


def send_verify_email(user):
    """
    Sends an email verification link to the specified user.
    """

    token_generator = PasswordResetTokenGenerator()

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    domain = settings.DOMAIN
    verify_url = f'{domain}/accounts/verify-email/{uid}/{token}'

    subject = 'Email Verification'
    message = render_to_string(
        'emails/verify_email.html',
        {
            'user': user,
            'verify_url': verify_url,
        }
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=message
    )