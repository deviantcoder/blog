import pytest

from blog.factories import PostFactory, ProfileFactory


@pytest.fixture
def posts():
    return PostFactory.create_batch(20)


@pytest.fixture
def user_posts():
    profile = ProfileFactory()
    return PostFactory.create_batch(20, author=profile)