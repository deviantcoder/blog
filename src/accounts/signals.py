import os
import shutil
import logging

from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth import get_user_model

from core.utils import send_log


logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_delete, sender=User)
def delete_user_media_files(sender, instance, **kwargs):
    try:
        path = f'media/users/{str(instance.id)[:8]}'
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        send_log(logger, f'Media deletion failed for: {instance.username}.', level='warning')