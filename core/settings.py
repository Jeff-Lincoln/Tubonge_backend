# Django settings for core project.
from pathlib import Path
import dj_database_url
from decouple import config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Stream API Configuration
API_GETSTREAM_PUBLIC_KEY = os.getenv('API_GETSTREAM_PUBLIC_KEY')
API_GETSTREAM_SECRET_KEY = os.getenv('API_GETSTREAM_SECRET_KEY')

# Secret key and debug settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(' ')

# Installed applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',
    'rest_framework',
    'channels',
    'corsheaders',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Static files settings for Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production

# URL configuration
ROOT_URLCONF = 'core.urls'

# Templates
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

# ASGI application
ASGI_APPLICATION = 'core.asgi.application'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)

# Database configuration with specified connection string
DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://tubonge_django_user:sXGNFHtDUa7o2ns8pmv4iFbnUd5O4QJU@dpg-csg2tbqj1k6c7388qrvg-a.oregon-postgres.render.com/tubonge_django",
        conn_max_age=600,
        ssl_require=True
    )
}

# Channels configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# # Django settings for core project.
# from pathlib import Path
# import dj_database_url
# from decouple import config
# from urllib.parse import urlparse
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Stream API Configuration
# API_GETSTREAM_PUBLIC_KEY = os.getenv('API_GETSTREAM_PUBLIC_KEY')
# API_GETSTREAM_SECRET_KEY = os.getenv('API_GETSTREAM_SECRET_KEY')

# # Quick-start development settings - unsuitable for production
# SECRET_KEY = config('SECRET_KEY')
# DEBUG = config('DEBUG', default=True, cast=bool)
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(' ')

# # Application definition
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'main_app',
#     'rest_framework',
#     'channels',
#     'corsheaders',
# ]

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# ]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ROOT_URLCONF = 'core.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# ASGI_APPLICATION = 'core.asgi.application'

# # CORS settings
# CORS_ALLOW_ALL_ORIGINS = True  # Change this in production

# CORS_ORIGIN_ALLOW_ALL = True

# # Database configuration
# tmpPostgres = urlparse(config("DATABASE_URL"))

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': tmpPostgres.path[1:],
#         'USER': tmpPostgres.username,
#         'PASSWORD': tmpPostgres.password,
#         'HOST': tmpPostgres.hostname,
#         'PORT': tmpPostgres.port or '5432',
#     }
# }

# DATABASES['default'] = dj_database_url.parse("postgresql://tubonge_django_user:sXGNFHtDUa7o2ns8pmv4iFbnUd5O4QJU@dpg-csg2tbqj1k6c7388qrvg-a.oregon-postgres.render.com/tubonge_django")



# # Channels configuration
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files (CSS, JavaScript, Images)
# STATIC_URL = 'static/'

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DEBUG = os.environ.get("DEBUG", "False").lower() == "true"