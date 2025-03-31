from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from blog.models import Post

from .models import Profile
from .forms import ProfileForm


User = get_user_model()


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


def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    posts = profile.posts.all().order_by('created')[:3]

    context = {
        'title': profile.display_name,
        'profile': profile,
        'posts': posts,
    }

    return render(request, 'profiles/profile.html', context)
