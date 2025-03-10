from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import LoginForm, RegisterForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()

    context = {
        'title': 'Sign In',
        'form': form,
    }

    return render(request, 'accounts/login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            user = authenticate(request, username=user.username, password=form.cleaned_data.get('password1'))

            login(request, user)

            return redirect('/')
    else:
        form = RegisterForm()

    context = {
        'title': 'Sign Up',
        'form': form,
    }

    return render(request, 'accounts/register.html', context)
