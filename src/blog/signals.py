import os
import shutil
import logging

from django.dispatch import receiver
from django.db.models.signals import post_delete

from core.utils import send_log

from .models import Post


logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Post)
def delete_post_media(sender, instance, **kwargs):
    try:
        path = f'media/posts/{str(instance.id)[:8]}'
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        send_log(logger, f'Media deletion failed for (post): {instance.id}', level='warning')