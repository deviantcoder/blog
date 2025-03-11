from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class SocialAccount(models.Model):
    """
    Model representing a social account linked to a user.
    Attributes:
        PROVIDER_CHOICES (tuple): Choices for the social account provider.
        user (ForeignKey): Reference to the user who owns the social account.
        provider (CharField): The provider of the social account (e.g., Google, GitHub).
        uid (CharField): Unique identifier for the social account.
        extra_data (JSONField): Additional data related to the social account.
    """

    PROVIDER_CHOICES = (
        ('google', 'Google'),
        ('github', 'GitHub'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')

    provider = models.CharField(max_length=10, choices=PROVIDER_CHOICES)
    uid = models.CharField(max_length=255, unique=True)

    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('provider', 'uid')

    def __str__(self):
        return f'{self.user.username} - {self.provider}'