from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .forms import LoginForm, RegisterForm


User = get_user_model()
token_generator = PasswordResetTokenGenerator()


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
            form.save()
            return render(
                request,
                'emails/verify_email_sent.html',
                {'title': 'Email sent'}
            )
    else:
        form = RegisterForm()

    context = {
        'title': 'Sign Up',
        'form': form,
    }

    return render(request, 'accounts/register.html', context)


def verify_email(request, uidb64, token):
    if request.user.is_authenticated and request.user.email_verified:
        return redirect('/')

    user = None
    try:
        uid_bytes = urlsafe_base64_decode(force_str(uidb64))
        uid_str = uid_bytes.decode('utf-8')
        user = User.objects.get(pk=uid_str)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, UnicodeDecodeError):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        if hasattr(user, 'email_verified'):
            user.email_verified = True
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'

        login(request, user)

        return redirect('/')
    
    elif user and not user.email_verified:
        user.delete()

    return render(
        request,
        'emails/verify_email_failed.html',
        {'title': 'Email failed'}
    )
