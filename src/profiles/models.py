import os
import logging
import shortuuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

from core.utils import validate_file_size, send_log, compress_image


ALLOWED_IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp')
DEFAULT_IMAGE_PATH = 'defaults/def.png'

User = get_user_model()

logger = logging.getLogger(__name__)


def upload_to(instance, filename):
    """
    Generates a file path for uploading user images.
    """
    
    ext = os.path.splitext(filename)[-1].lower()
    new_filename = shortuuid.uuid()[:8]

    return f'profiles/{str(instance.pk)[:8]}/{new_filename}{ext}'


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', primary_key=True
    )
    display_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(
        default=DEFAULT_IMAGE_PATH,
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(ALLOWED_IMAGE_EXTENSIONS),
            validate_file_size,
        ],
        blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if is_new and not self.display_name:
            self.display_name = self.user.username

        if not is_new and self.image:
            try:
                old_instance = Profile.objects.get(user=self.user)
                if old_instance.image == self.image:
                    super().save(*args, **kwargs)
                    return
            except Profile.DoesNotExist:
                send_log(logger, f'Profile for user {self.user.id} not found during update.', level='warning')

        if self.image and self.image.name != DEFAULT_IMAGE_PATH:
            try:
                self.image = compress_image(self.image)
            except Exception as e:
                send_log(logger, f'Image compression failed for profile {self.user.username}: {e}', level='error')

        super().save(*args, **kwargs)
