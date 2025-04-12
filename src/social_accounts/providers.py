import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


DEFAULT_PROVIDER_CONFIG = {
    'UID_FIELD': 'id',
    'USERNAME_FROM': 'email',
    'AUTH_HEADER_FORMAT': 'Bearer {token}',
    'TOKEN_PARAMS': {'grant_type': 'authorization_code'},
    'USERINFO_PARAMS': {},
    'SCOPE': 'email',
}


class ProviderConfig:
    def __init__(self, name, config):
        self.name = name
        self.config = {**DEFAULT_PROVIDER_CONFIG, **config}
        self.validate_config()

    def validate_config(self):
        required = [
            'AUTH_URI',
            'TOKEN_URI',
            'USERINFO_URI',
            'CLIENT_ID',
            'CLIENT_SECRET',
            'REDIRECT_URI',
        ]

        missing = [field for field in required if field not in self.config]

        if missing:
            raise ImproperlyConfigured(
                f'Provider {self.name} missing: {', '.join(missing)}'
            )
        
    def __getattr__(self, attr):
        try:
            return self.config[attr]
        except KeyError:
            raise AttributeError(f'No config {attr} for provider {self.name}')
        

class ProviderRegistry:
    def __init__(self):
        self._providers = {}

    def register(self, name, **config):
        self._providers[name] = ProviderConfig(name, config)

    def get(self, name):
        provider = self._providers.get(name)

        if not provider:
            raise ValueError(f'Provider {name} is not registered')
        return provider
    

registry = ProviderRegistry()


def autodiscover_providers():
    for provider_name, config in getattr(settings, 'SOCIAL_AUTH_PROVIDERS', {}).items():
        registry.register(provider_name, **config)


autodiscover_providers()
