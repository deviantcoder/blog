import secrets

from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages

from .services import OAuthService


def oauth_login(request, provider):
    try:
        state = secrets.token_urlsafe(32)
        request.session['oauth_state'] = state

        oauth = OAuthService(provider)
        return redirect(oauth.get_auth_url(state=state))
    except Exception as e:
        messages.error(request, 'Authentication service unavailable')
        return redirect('accounts:login')


def oauth_callback(request, provider):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code or (not state or state != request.session.pop('oauth_state', None)):
        messages.error(request, 'Invalid authentication request')
        return redirect('accounts:login')

    try:
        oauth = OAuthService(provider)
        token = oauth.get_access_token(code)
        user_data = oauth.get_user_info(token)
        user = oauth.get_or_create_user(user_data)
        
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        messages.success(request, 'Logged in successfully')

        return redirect('/')
    except Exception as e:
        messages.error(request, 'Authentication failed')

        return redirect('accounts:login')