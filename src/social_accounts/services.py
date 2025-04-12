import requests

from django.contrib.auth import get_user_model

from .models import SocialAccount
from .providers import registry


User = get_user_model()


class OAuthService:
    def __init__(self, provider_name):
        self.provider = registry.get(provider_name)

    def get_auth_url(self, state):
        params = {
            'client_id': self.provider.CLIENT_ID,
            'redirect_uri': self.provider.REDIRECT_URI,
            'response_type': 'code',
            'scope': self.provider.SCOPE,
            'state': state,
        }

        return f'{self.provider.AUTH_URI}?{'&'.join(f'{k}={v}' for k, v in params.items())}'
    
    def get_access_token(self, code):
        token_data = {
            'code': code,
            'client_id': self.provider.CLIENT_ID,
            'client_secret': self.provider.CLIENT_SECRET,
            'redirect_uri': self.provider.REDIRECT_URI,
            **self.provider.TOKEN_PARAMS
        }

        response = requests.post(
            self.provider.TOKEN_URI,
            data=token_data,
            headers={'Accept': 'application/json'}
        )

        return response.json().get('access_token')
    
    def get_user_info(self, access_token):
        headers = {
            'Authorization': self.provider.AUTH_HEADER_FORMAT.format(token=access_token)
        }

        response = requests.get(
            self.provider.USERINFO_URI,
            headers=headers,
            params=self.provider.USERINFO_PARAMS
        )

        return self._normalize_user_data(response.json())
    
    def _normalize_user_data(self, data):
        if self.provider.USERNAME_FROM == 'email' and 'email' in data:
            data['username'] = data['email'].split('@')[0]
        elif isinstance(self.provider.USERNAME_FROM, str):
            data['username'] = data.get(self.provider.USERNAME_FROM, '')

        if not data.get('email') and hasattr(self.provider, 'EMAIL_FALLBACK'):
            data['email'] = self.provider.EMAIL_FALLBACK(data)

        return data
    
    def get_or_create_user(self, user_data):
        uid = str(user_data.get(self.provider.UID_FIELD))
        email = user_data.get('email', '')
        username = user_data.get('username', '')

        try:
            social_account = SocialAccount.objects.get(provider=self.provider.name, uid=uid)
            return social_account.user
        except SocialAccount.DoesNotExist:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'email_verified': True,
                    'is_active': True,
                }
            )
            
            SocialAccount.objects.create(
                provider=self.provider.name,
                uid=uid,
                user=user,
                extra_data=user_data
            )

            return user
