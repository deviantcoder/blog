import os
import shortuuid

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.conf import settings

from core.utils import compress_image ,validate_file_size


ALLOWED_IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp')
DEFAULT_IMAGE_PATH = 'defaults/def.png'


def upload_to(instance, filename):
    """
    Generates a file path for uploading user images.
    """
    
    ext = os.path.splitext(filename)[-1].lower()
    new_filename = shortuuid.uuid()[:8]

    return f'users/{str(instance.id)[:8]}/{new_filename}{ext}'


class AppUser(AbstractUser):
    """
    AppUser model extends the AbstractUser model to include additional fields and functionality.
    """

    display_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(
        default=DEFAULT_IMAGE_PATH,
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(ALLOWED_IMAGE_EXTENSIONS),
            validate_file_size(settings.MAX_IMAGE_SIZE),
        ],
        blank=True
    )

    email_verified = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['username'], name='appuser_username_idx'),
        ]

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if is_new and not self.display_name:
            self.display_name = self.username

        if not is_new and self.image:
            try:
                old_instance = AppUser.objects.get(id=self.id)
                if old_instance.image == self.image:
                    super().save(*args, **kwargs)
                    return
            except AppUser.DoesNotExist:
                pass # logging will be here

        if self.image and self.image != DEFAULT_IMAGE_PATH:
            try:
                self.image = compress_image(self.image)
            except Exception as e:
                pass # logging will be here

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        pass