import pytest

from django.urls import reverse
from django.utils import timezone


@pytest.mark.django_db
def test_start_end_date_filter(user_posts, client):
    # start date check

    start_date_cutoff = timezone.now() - timezone.timedelta(days=60)
    
    GET_params = {'start_date': start_date_cutoff}

    response = client.get(reverse('blog:posts_list'), GET_params)

    qs = response.context['filter'].qs

    for post in qs:
        assert post.created >= start_date_cutoff

    # end date check

    end_date_cutoff = timezone.now() - timezone.timedelta(days=20)
    
    GET_params = {'end_date': end_date_cutoff.date()}

    response = client.get(reverse('blog:posts_list'), GET_params)

    qs = response.context['filter'].qs

    for post in qs:
        assert post.created <= end_date_cutoff

    # end date and start date check

    start_date_cutoff = timezone.now() - timezone.timedelta(days=70)
    end_date_cutoff = timezone.now() - timezone.timedelta(days=20)

    GET_params = {
        'start_date': start_date_cutoff.date(),
        'end_date': end_date_cutoff.date(),
    }

    response = client.get(reverse('blog:posts_list'), GET_params)

    qs = response.context['filter'].qs

    for post in qs:
        assert start_date_cutoff <= post.created <= end_date_cutoff
