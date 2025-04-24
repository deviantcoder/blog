import os
import logging

from io import BytesIO

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from PIL import Image

logger = logging.getLogger(__name__)


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
        send_log(logger, 'Image compression failed', level='warning')


def validate_file_size(file):
    """
    Validates the size of the given file against the maximum allowed size.
    """

    max_size_bytes = settings.MAX_IMAGE_SIZE * 1024 * 1024  # Convert MB to bytes
    current_size_mb = file.size / (1024 * 1024)
    
    if file.size > max_size_bytes:
        raise ValidationError(f'File size cannot exceed {settings.MAX_IMAGE_SIZE:.2f} MB. Current file size: {current_size_mb:.2f} MB')


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


def send_log(logger: logging.Logger, message: str = None, level: str = 'info'):
    """
    Sends a log message to the specified logger at the given log level.
    """

    LEVEL_MAP = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    try:
        log_level = LEVEL_MAP.get(level.lower().strip())
    except KeyError:
        raise ValueError(f'Invalid log level: {level}')

    return logger.log(log_level, message)


def paginate(request, objects, per_page=10):
    """
    Paginate a queryset or list of objects, returning 
    the page and a custom range of page numbers.
    """

    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    left_index = max(1, int(page) - 2)
    right_index = min(paginator.num_pages + 1, int(page) + 3)

    custom_range = range(left_index, right_index)

    return objects, custom_range, paginator
