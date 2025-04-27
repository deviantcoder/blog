import pytest

from datetime import datetime, timedelta

from django.urls import reverse


@pytest.mark.django_db
def test_start_end_date_filter(user_posts, client):
    user = user_posts[0].author.user
    client.force_login(user)

    start_date_cutoff = datetime.now() - timedelta(days=30)

    GET_params = {'start_date': start_date_cutoff}
    response = client.get(reverse('blog:posts_list'), GET_params)

    qs = response.context['filter'].qs
