import os
import uuid
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from PIL import Image

from .models import DEFAULT_IMAGE_PATH, AppUser, upload_to


class AppUserModelTest(TestCase):

    def setUp(self):
        self.user = AppUser.objects.create(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.display_name, 'testuser')
        self.assertEqual(self.user.image.name, DEFAULT_IMAGE_PATH)
        self.assertFalse(self.user.email_verified)
        self.assertTrue(isinstance(self.user.id, uuid.UUID))

    def test_str_method(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_display_name_not_set(self):
        user = AppUser(username='newuser')
        user.save()
        self.assertEqual(user.display_name, 'newuser')

    def test_display_name_set(self):
        user = AppUser(username='newuser', display_name='New User')
        user.save()
        self.assertEqual(user.display_name, 'New User')

    def test_upload_to(self):
        filename = 'testimage.jpg'
        path = upload_to(self.user, filename)

        self.assertTrue(path.startswith(f'users/{str(self.user.id)[:8]}/'))
        self.assertTrue(path.endswith('.jpg'))
        self.assertEqual(len(os.path.basename(path).split('.')[0]), 8)

    def test_image_default(self):
        self.assertEqual(self.user.image.name, DEFAULT_IMAGE_PATH)

    def test_valid_image_upload(self):
        image = Image.new('RGB', (100, 100), 'white')
        img_io = BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)

        uploaded_file = SimpleUploadedFile(
            'test.png',
            img_io.read(),
            content_type='image/png'
        )

        self.user.image = uploaded_file
        self.user.save()
        
        self.assertTrue(self.user.image.name.endswith('.jpg'))
        self.assertTrue(os.path.exists(self.user.image.path))

    def test_invalid_file_extension(self):
        invalid_file = SimpleUploadedFile(
            'test.txt',
            b'some random text',
            content_type='text/plain'
        )

        self.user.image = invalid_file
        
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_file_size_exceeds_limit(self):
        big_file = SimpleUploadedFile(
            'big_image.jpg',
            b'0' * (settings.MAX_IMAGE_SIZE + 1) * 1024 * 1024,
            content_type='image/jpeg'
        )

        self.user.image = big_file

        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_image_not_recompressed_if_unchanged(self):
        image = Image.new('RGB', (100, 100), 'white')
        img_io = BytesIO()

        image.save(img_io, format='PNG')
        img_io.seek(0)

        uploaded_file = SimpleUploadedFile(
            'test.png',
            img_io.read(),
            content_type='image/png'
        )

        self.user.image = uploaded_file
        self.user.save()

        original_path = self.user.image.path
        original_mtime = os.path.getmtime(original_path)

        self.user.save()

        self.assertEqual(self.user.image.path, original_path)
        self.assertEqual(os.path.getmtime(original_path), original_mtime)