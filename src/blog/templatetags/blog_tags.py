import re
import uuid
import markdown

from django import template
from django.utils.safestring import mark_safe

from blog.models import Post

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(text):
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.fenced_code',
    ]
    return mark_safe(markdown.markdown(text, extensions=extensions))


@register.filter(name='plaintext')
def plaintext_filter(text):
    html = markdown.markdown(text)

    plain = re.sub(r'<[^>]+>', '', html)
    plain = re.sub(r'\s+', ' ', plain).strip()

    return plain


@register.filter(name='get_post_by_id')
def get_post_by_id(posts, post_id):
    try:
        post_uuid = uuid.UUID(post_id)
        return posts.get(id=post_uuid)
    except (ValueError, Post.DoesNotExist):
        return Post.objects.filter(id=post_id).first()
