from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY', cast=str)

DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = ['*']

DOMAIN = DOMAIN = config('DOMAIN', cast=str, default='http://127.0.0.1:8000')

# Email config

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', cast=str, default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', cast=str, default='587')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool, default=False)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str, default='jamessullivanpost@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str)

# OAuth config (Google, GitHub)

GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', cast=str)
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET', cast=str)
GOOGLE_REDIRECT_URI = 'http://127.0.0.1:8000/social/oauth/google/callback'
GOOGLE_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URI = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URI = 'https://www.googleapis.com/oauth2/v3/userinfo'

GITHUB_CLIENT_ID = config('GITHUB_CLIENT_ID', cast=str)
GITHUB_CLIENT_SECRET = config('GITHUB_CLIENT_SECRET', cast=str)
GITHUB_REDIRECT_URI = 'http://127.0.0.1:8000/social/oauth/github/callback/'
GITHUB_AUTH_URI = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URI = 'https://github.com/login/oauth/access_token'
GITHUB_USERINFO_URI = 'https://api.github.com/user'

# Elasticsearch config

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://127.0.0.1:9200/'
    },
}

# Django Rest Framework config

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3-rd party

    'crispy_forms',
    'crispy_bootstrap5',
    'django_elasticsearch_dsl',
    'mptt',
    'rest_framework',
    'silk',

    # apps

    'accounts.apps.AccountsConfig',
    'social_accounts.apps.SocialAccountsConfig',
    'profiles.apps.ProfilesConfig',
    'commands.apps.CommandsConfig',
    'blog.apps.BlogConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 3-rd party
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Auth config

AUTH_USER_MODEL = 'accounts.AppUser'

AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

PROFILE_USER_MODEL = 'profiles.Profile'

# Logging config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d %(module)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG', # or INFO
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/debug.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'accounts': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False, # could be True
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Crispy forms

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True


# Static files

STATIC_URL = 'static/'

STATICFILES_BASE_DIR = BASE_DIR / 'static'
STATICFILES_BASE_DIR.mkdir(exist_ok=True, parents=True)

STATICFILES_VENDOR_DIR = STATICFILES_BASE_DIR / 'vendor'

STATICFILES_DIRS = [
    STATICFILES_BASE_DIR,
]

STATIC_ROOT = 'local_cdn'

# Media config

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

MAX_IMAGE_SIZE = 10

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
