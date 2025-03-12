from django.shortcuts import render


def home_feed_view(request):
    context = {
        'title': 'Feed',
    }

    return render(request, 'blog/home_feed.html', context)
