import logging

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser


logger = logging.getLogger(__name__)


class AppUser(AbstractUser):
    """
    AppUser model extends the AbstractUser model to include additional fields and functionality.
    """

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

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        pass