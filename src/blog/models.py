import os
import logging
import shortuuid

from uuid import uuid4

from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.db import transaction
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey

from core.utils import validate_file_size, send_log, compress_image


logger = logging.getLogger(__name__)

ALLOWED_IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp')
DEFAULT_IMAGE_PATH = 'defaults/def.png'


def upload_to(instance, filename):
    """
    Generates a file path for uploading post images.
    """
    
    ext = os.path.splitext(filename)[-1].lower()
    new_filename = shortuuid.uuid()[:8]

    return f'posts/{str(instance.id)[:8]}/{new_filename}{ext}'


class Post(models.Model):
    """
    Post model represents a blog post with attributes such as author,
    title, content, header image, status, and timestamps.
    """

    POST_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(
        settings.PROFILE_USER_MODEL, on_delete=models.SET_NULL, related_name='posts', null=True
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    header_image = models.ImageField(
        upload_to=upload_to,
        validators=[
            FileExtensionValidator(ALLOWED_IMAGE_EXTENSIONS),
            validate_file_size,
        ],
        null=True,
        blank=True
    )

    status = models.CharField(max_length=10, choices=POST_STATUS, default='draft')

    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField(max_length=100, unique=True, blank=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['slug'], name='post_slug_idx')
        ]

    def __str__(self):
        return f'{self.author.user. username}: {self.title[:20]}'
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if not self.slug:
            with transaction.atomic():
                base_slug = slugify(self.title)[:80]

                if Post.objects.filter(slug=base_slug).exists():
                    slug = f'{base_slug}_{shortuuid.uuid()[:8]}'
                else:
                    slug = base_slug
                self.slug = slug

        if not is_new and self.header_image:
            try:
                old_instance = Post.objects.get(id=self.id)
                if old_instance.header_image == self.header_image:
                    super().save(*args, **kwargs)
                    return
            except Post.DoesNotExist:
                send_log(logger, f'Instance with id {self.id} not found during update.', level='warning')

        if self.header_image:
            try:
                self.header_image = compress_image(self.header_image)
            except Exception as e:
                send_log(logger, f'Image compression failed for (post): {self.id}: {e}.', level='error')

        super().save(*args, *kwargs)

    @property
    def get_created(self):
        return self.created.strftime('%B %d, %Y')
    
    def get_absolute_url(self):
        return reverse('blog:view_post', kwargs={'slug': self.slug})


class Comment(MPTTModel):
    """
    Represents a comment in a blog post, supporting threaded replies using MPTT.
    """

    author = models.ForeignKey(
        settings.PROFILE_USER_MODEL, on_delete=models.SET_NULL, related_name='comments', null=True
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    body = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ('-created',)

    class MPTTMeta:
        order_insertion_by = ['post']

    def __str__(self):
        return f'{self.author.display_name}: {self.body[:50]}'
    

class Upvote(models.Model):
    """
    Represents an upvote on a blog post by a user profile.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='upvotes')
    profile = models.ForeignKey(
        settings.PROFILE_USER_MODEL, on_delete=models.SET_NULL, related_name='upvotes', null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        unique_together = ('post', 'profile')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.profile.display_name}: {self.post.title[:50]}'


class Tag(models.Model):
    """
    Represents a Tag model used for categorizing/labeling content.
    """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
