import io
import factory

from PIL import Image

from blog.models import Post, Tag
from accounts.models import AppUser
from profiles.models import Profile

from django.core.files.uploadedfile import SimpleUploadedFile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AppUser
        django_get_or_create = ('username', 'email')

    username = factory.Sequence(lambda n: f'test_user{n}')
    email = factory.Sequence(lambda n: f'test_user{n}@gmail.com')
    email_verified = True
    is_active = True


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ('user',)
    
    user = factory.SubFactory(UserFactory)
    image = SimpleUploadedFile(
        'test.jpg',
        b'static',
        content_type='image/jpeg'
    )


def get_test_image():
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), 'blue')
    image.save(file, 'jpeg')
    file.name = 'test.jpg'
    file.seek(0)
    return SimpleUploadedFile('test.jpg', file.read(), content_type='image/jpeg')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(ProfileFactory)
    title = factory.Faker('sentence', nb_words=5)
    content = factory.Faker('paragraph', nb_sentences=10)
    status = 'published'

    header_image = factory.LazyFunction(get_test_image)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Faker('word')
