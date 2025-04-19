import django_filters

from .models import Post, Tag

from django import forms


class PostFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        label='Date From',
        widget=forms.DateTimeInput(attrs={'type': 'date'})
    )

    end_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='lte',
        label='Date To',
        widget=forms.DateTimeInput(attrs={'type': 'date'})
    )

    tags = django_filters.ModelMultipleChoiceFilter(
        label='Filter by Tags',
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Post
        fields = (
            'start_date',
            'end_date',
            'tags',
        )