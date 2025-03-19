from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Post


@registry.register_document
class PostDocument(Document):
    title = fields.TextField(analyzer='standard')
    content = fields.TextField(analyzer='standard')
    author_display_name = fields.TextField(attr='author.display_name')
    created = fields.DateField()

    class Index:
        name = 'posts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Post
        fields = ['id', 'slug', 'status']
        related_models = ['profiles.Profile']

    def prepare_author_display_name(self, instance):
        return instance.author.display_name
    