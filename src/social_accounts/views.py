import requests

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.urls import reverse

from .models import SocialAccount


User = get_user_model()


def oauth_login(request, provider):
    """
    Redirect user to the OAuth provider's authorization page.
    """

    if provider == 'google':
        auth_uri = settings.GOOGLE_AUTH_URI
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        scope = 'openid email profile'
    elif provider == 'github':
        auth_uri = settings.GITHUB_AUTH_URI
        client_id = settings.GITHUB_CLIENT_ID
        redirect_uri = settings.GITHUB_REDIRECT_URI
        scope = 'user:email'
    else:
        messages.warning(request, 'Social sign in failed')
        return redirect('accounts:login')

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
        'state': 'random_string_for_csrf_protection',
    }

    auth_url = f"{auth_uri}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    return redirect(auth_url)

def oauth_callback(request, provider):
    """
    Handle the callback from the OAuth provider.
    """

    code = request.GET.get('code')

    if not code:
        messages.warning(request, 'Social sign in failed')
        return redirect('accounts:login')

    if provider == 'google':
        token_uri = settings.GOOGLE_TOKEN_URI
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        userinfo_uri = settings.GOOGLE_USERINFO_URI
    elif provider == 'github':
        token_uri = settings.GITHUB_TOKEN_URI
        client_id = settings.GITHUB_CLIENT_ID
        client_secret = settings.GITHUB_CLIENT_SECRET
        redirect_uri = settings.GITHUB_REDIRECT_URI
        userinfo_uri = settings.GITHUB_USERINFO_URI
    else:
        return redirect('accounts:login')

    token_data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    
    if provider == 'github':
        headers = {'Accept': 'application/json'}
        token_response = requests.post(token_uri, data=token_data, headers=headers)
    else:
        token_response = requests.post(token_uri, data=token_data)

    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if not access_token:
        messages.warning(request, 'Social sign in failed')
        return redirect('accounts:login')

    # fetch user info

    headers = {'Authorization': f'Bearer {access_token}' if provider == 'google' else f'token {access_token}'}
    user_response = requests.get(userinfo_uri, headers=headers)
    user_data = user_response.json()

    # get user info

    if provider == 'google':
        email = user_data.get('email')
        uid = user_data.get('sub')
        username = email.split('@')[0]
    elif provider == 'github':
        email = user_data.get('email')
        uid = str(user_data.get('id'))
        username = user_data.get('login')

        if not email:
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers={'Authorization': f'token {access_token}'}
            )

            emails = email_response.json()

            for e in emails:
                if e.get('primary') and e.get('verified'):
                    email = e['email']
                    break
                
            if not email:
                email = f"{username}@github.placeholder"

    # get or create user

    try:
        social_account = SocialAccount.objects.get(provider=provider, uid=uid)
        user = social_account.user
    except SocialAccount.DoesNotExist:
        try:
            user = User.objects.get(email=email)
            social_account = SocialAccount.objects.create(
                provider=provider,
                uid=uid,
                user=user,
                extra_data=user_data
            )
        except User.DoesNotExist:
            user = User.objects.create(
                username=username,
                email=email,
                email_verified=True,
                is_active=True,
            )
            social_account = SocialAccount.objects.create(
                provider=provider,
                uid=uid,
                user=user,
                extra_data=user_data
            )
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email=email).first()
            social_account = SocialAccount.objects.create(
                provider=provider,
                uid=uid,
                user=user,
                extra_data=user_data
            )

    user.backend = 'accounts.backends.EmailOrUsernameModelBackend'

    login(request, user)

    return redirect('/')