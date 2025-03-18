from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from blog.models import Post

from .forms import ProfileForm


@login_required(login_url='accounts:login')
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('/')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'title': 'Edit Profile',
        'form': form,
    }

    return render(request, 'profiles/edit_profile.html', context)


def profile_settings(request):
    context = {
        'title': 'Settings',
        'published_posts': Post.objects.filter(author=request.user.profile, status='published'),
        'draft_posts': Post.objects.filter(author=request.user.profile, status='draft'),
    }
    return render(request, 'profiles/settings.html', context)
