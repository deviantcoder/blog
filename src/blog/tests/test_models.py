import uuid

import pytest

from blog.models import Post
from blog.factories import (
    PostFactory, ProfileFactory, TagFactory, get_test_image
)

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError


@pytest.mark.django_db
def test_post_creation():
    post = PostFactory(
        title = 'Test Post',
        content = 'Test Content',
    )

    assert post.title == 'Test Post'
    assert post.content == 'Test Content'
    assert post.slug
    assert isinstance(post.id, uuid.UUID)


@pytest.mark.django_db
def test_post_slug_generation():
    post_1 = PostFactory(title='Test Post')
    post_2 = PostFactory(title='Test Post')

    assert post_1.slug != post_2.slug
    assert 'test-post' in post_1.slug
    assert 'test-post' in post_2.slug


@pytest.mark.django_db
def test_post_image_upload():
    image = get_test_image()
    post = PostFactory(header_image=image)

    assert post.header_image.name.endswith('.jpg')


@pytest.mark.django_db
def test_post_image_compression():
    image = get_test_image()
    post = PostFactory(header_image=image)

    assert post.header_image.size < image.size


@pytest.mark.django_db
def test_post_author_relationship():
    profile = ProfileFactory()
    post = PostFactory(author=profile)

    assert post.author == profile
    assert post.author.user == profile.user
    assert post in profile.posts.all()


@pytest.mark.django_db
def test_post_tag_relationship():
    tag = TagFactory()
    post = PostFactory()

    post.tags.add(tag)

    assert tag in post.tags.all()
    assert post in tag.posts.all()


@pytest.mark.django_db
def test_post_save_with_existing_slug():
    PostFactory(title='Duplicate', slug='forced-slug')

    with pytest.raises(IntegrityError):
        PostFactory(title='Duplicate', slug='forced-slug')


@pytest.mark.django_db
def test_post_save_without_image_change():
    post = PostFactory()
    original_image = post.header_image

    post.save()

    assert post.header_image == original_image
    assert post.header_image.size == original_image.size
