import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.environ.get("SECRET_KEY",
                                default='django-insecure-#k+78%hwvigmg50o=1vrbi+2$um&pr*2yez=1a2_+jw4bh)4h+'))

DEBUG = bool(int(os.environ.get("DEBUG", default=1)))

ALLOWED_HOSTS = str(os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    default='localhost 127.0.0.1 backend'
)).split(" ")

CSRF_TRUSTED_ORIGINS = str(os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    default='https://*.localhost:8000 https://*.127.0.0.1:8000 http://localhost:8000 http://127.0.0.1:8000 '
            'https://*.localhost:8080 https://*.127.0.0.1:8080 http://localhost:8080 http://127.0.0.1:8080'
)).split(" ")

CORS_ALLOWED_ORIGINS = str(os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    default='https://*.localhost:8000 https://*.127.0.0.1:8000 http://localhost:8000 http://127.0.0.1:8000 '
            'https://*.localhost:8080 https://*.127.0.0.1:8080 http://localhost:8080 http://127.0.0.1:8080'
)).split(" ")

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Encoding',
    'Authorization',
    'Content-Type',
    'Origin',
    'X-CSRFToken',
    'X-Requested-With',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'corsheaders',
    'tinymce',

    'drf_spectacular',

    'users.apps.UsersConfig',
    'api_v1.apps.ApiV1Config'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend_config.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("POSTGRES_ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.environ.get("POSTGRES_DB", default="vkrback"),
        "USER": os.environ.get("POSTGRES_USER", default="vkrback"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", default="1234"),
        "HOST": os.environ.get("POSTGRES_HOST", default="localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", default="5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = [
    'users.backends.CustomUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

DJOSER = {
    'USER_ID_FIELD': 'username',
    'LOGIN_FIELD': 'username',
    'SERIALIZERS': {
        'user_create': 'users.serializers.CustomUserCreateSerializer',
        'user': 'users.serializers.CustomUserSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
        'token_create': 'users.serializers.CustomTokenCreateSerializer',
    },
    'TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'VKR',
    'DESCRIPTION': 'VKR backend api interface',
    'VERSION': '1.0.0',
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}
