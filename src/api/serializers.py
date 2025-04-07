from rest_framework import serializers

from blog.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
        )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    # tags = TagSerializer(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True)
    created = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'tags',
            'created',
            'url',
        )

    def get_created(self, obj):
        return obj.created.strftime('%Y-%m-%d')
    
    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())