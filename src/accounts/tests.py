import os
import uuid
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from PIL import Image

from .models import AppUser


class AppUserModelTest(TestCase):

    def setUp(self):
        self.user = AppUser.objects.create(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertFalse(self.user.email_verified)
        self.assertTrue(isinstance(self.user.id, uuid.UUID))

    def test_str_method(self):
        self.assertEqual(str(self.user), 'testuser')
