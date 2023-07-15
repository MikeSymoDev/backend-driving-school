"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-zc=$l+6f1x7gig%!c7#6idf#bdo_0f0g9nzk3oyg_*k2)i(v60'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
print(DEBUG)

SERVER_TYPE = os.environ.get('SERVER_TYPE', 'development')

ALLOWED_HOSTS = ['backend-driving-school-99d5f092ee9a.herokuapp.com']

if SERVER_TYPE !='production':
    ALLOWED_HOSTS += ['127.0.0.1']

CORS_ALLOWED_ORIGINS = ['https://fe-driving-school-83b8d520b244.herokuapp.com', 'http://localhost:3000']

if SERVER_TYPE != 'production':
    CORS_ALLOWED_ORIGINS += ['http://localhost:3000']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # own apps
    'user',
    'userProfile',
    'vehicle',
    'vehicleImage',
    'appointment',
    'availableTime',
    'class_package',
    'drivingSchool',



    # Third party Apps
    'rest_framework',
    'drf_yasg',
    'corsheaders',
]

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        "PORT": os.environ.get('POSTGRES_PORT'),
        "HOST": os.environ.get('POSTGRES_HOST'),
        "USER": os.environ.get('POSTGRES_USER'),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
    }
}

if SERVER_TYPE == 'production':
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

if SERVER_TYPE == 'production':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # AWS SDK
    AWS_ACCESS_KEY_ID = os.environ.get('DO_SPACES_ACCESS_KEY')  # Spaces access key
    AWS_SECRET_ACCESS_KEY = os.environ.get('DO_SPACES_SECRET')  # Spaces access secret
    AWS_STORAGE_BUCKET_NAME = os.environ.get('DO_SPACES_SPACE_NAME')  # Name of the space
    AWS_S3_ENDPOINT_URL = os.environ.get('DO_SPACES_ENDPOINT')  # Endpoint of DO spaces
    MEDIA_URL = 'https://backend-driving-school.fra1.digitaloceanspaces.com/media/'  # Full url displayed in Spaces + your media folder

else:
    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2)
}

# SWAGGER_SETTINGS = {
#     'USE_SESSION_AUTH': False,  # Change settings to True to enable Django Login option
#     'LOGIN_URL': 'admin/',  # URL For Django Login
#     'LOGOUT_URL': 'admin/logout/',  # URL For Django Logout
#     'SECURITY_DEFINITIONS': {  # Allows usage of Access token to make requests on the docs.
#         'Bearer': {
#             'type': 'apiKey',
#             'name': 'Authorization',
#             'in': 'header'
#         }
#     }
# }