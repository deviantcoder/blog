import os
import shutil

from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(post_delete, sender=User)
def delete_user_media_files(sender, instance, **kwargs):
    try:
        path = f'media/users/{str(instance.id)[:8]}'
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        pass # logging will be here