import os
import shutil
import logging

from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.contrib.auth import get_user_model

from core.utils import send_log

from .models import Profile


logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            display_name=instance.username
        )


@receiver(post_delete, sender=Profile)
def delete_profile_media_files(sender, instance, **kwargs):
    try:
        path = f'media/profiles/{str(instance.pk)[:8]}'
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        send_log(logger, f'Media deletion failed for: {instance.username}.', level='warning')