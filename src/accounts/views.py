from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import LoginForm


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
