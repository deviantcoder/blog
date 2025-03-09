import os
from io import BytesIO

from django.core.files import File
from django.core.exceptions import ValidationError

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