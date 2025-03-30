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
