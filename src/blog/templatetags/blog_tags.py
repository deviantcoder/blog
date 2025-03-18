import re
import markdown

from django import template
from django.utils.safestring import mark_safe

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
