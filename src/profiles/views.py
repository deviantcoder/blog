from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from blog.models import Post
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

@login_required(login_url='accounts:login')
def profile_settings(request):
    user = request.user
    if request.method == 'POST':
        if 'update_username' in request.POST:
            new_username = request.POST.get('username')

            if not new_username:
                messages.warning(request, 'Username cannot be empty')
            elif new_username == user.username:
                messages.warning(request, 'This is already your username')
            elif User.objects.filter(username=new_username).exists():
                messages.warning(request, 'This username is already taken')
            else:
                user.username = new_username
                user.save()
                messages.success(request, 'Username updated')

            return redirect('profiles:settings')
    
        if 'update_image' in request.POST:
            new_image = request.FILES.get('image')

            if new_image:
                user.profile.image = new_image
                user.profile.save()
                messages.success(request, 'Profile picture updated')

            return redirect('profiles:settings')

    context = {
        'title': 'Settings',
        'published_posts': Post.objects.filter(author=request.user.profile, status='published'),
        'draft_posts': Post.objects.filter(author=request.user.profile, status='draft'),
    }

    return render(request, 'profiles/settings.html', context)
