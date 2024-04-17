"""
Django settings for flowka project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from os.path import abspath, dirname, join
import os
import sys
import json
from django.core.exceptions import ImproperlyConfigured




def root(*dirs):
    base_dir=join(dirname(__file__),'..')
    return abspath(join(base_dir,*dirs))


with open(join(root(),'secrets.json')) as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    try:
        secret=secrets[setting]
        if secret.lower()=='false':
            return False
        elif secret.lower()=='true':
            return True
        else:
            return secret
    except KeyError:
        error_msg = 'set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)

ADMINS=((get_secret("ADMIN_NAME"),get_secret("ADMIN_EMAIL")),)
MANAGERS=ADMINS
SITE_ID=1
SITE_URL='http://75.ilgigrad.net:8000'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = root()
BASE_DIR=dirname(root())
MEDIA_ROOT = root('uploads')
MEDIA_URL='/uploads/'

#STATICFILES_DIRS = []
APPS_DIR = root('apps')
sys.path.append(APPS_DIR)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATICFILES_DIRS = [join(APPS_DIR,"static")]

STATIC_URL = '/static/'
STATIC_ROOT = root('static')


#----------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
#------------------------------------------------------------------
#python command to generate a new key
#$ python
#>>>import random, string
#>>>"".join([random.choice("FlowkaDigitalCreativeIntelligence") for b in range(20)]) #in development eg
#>>>>>>"".join([random.choice(string.printable) for b in range(30)]) #in production
# copy and paste the key
#------------------------------------------------------------------
SECRET_KEY = get_secret("SECRET_KEY")
#------------------------------------------------------------------------

#------------------------------------------------------------------------
# COOKIES
#------------------------------------------------------------------------

SESSION_COOKIE_AGE = 60 * 60 * 2
# 2 HOURS
SESSION_COOKIE_HTTPONLY=True
#CSRF_COOKIE_DOMAIN='flowka.com'
#SESSION_ENGINE="django.contrib.sessions.backends.cached_db" #cache+insert in db =>more secure, slower
SESSION_ENGINE="django.contrib.sessions.backends.cached_db"#simple cache only=>faster
#------------------------------------------------------------------------

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '127.0.1.1',
    'www.ilgigrad.net',
    '75.ilgigrad.net',
    'ilgigrad.net',
    'django.ilgigrad.net',
    'django.75.ilgigrad.net']



# Application definition

DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
]

PACKAGED_APPS=[
    'widget_tweaks',
    'django_cleanup',
    'django_countries',
    'tagulous',
    'rest_framework',
    'django_tables2',
]

PROJECT_APPS=[

    'account.apps.AccountConfig',
    'store.apps.StoreConfig',
    'home.apps.HomeConfig',
    'core.apps.CoreConfig',
    'filer.apps.FilerConfig',
    'datacollect.apps.datacollectConfig',
    'rabbitMQ.apps.RabbitMQConfig',
    'tag.apps.TagConfig',
    'message.apps.MessageConfig',
    'survey.apps.SurveyConfig',
]

INSTALLED_APPS=DJANGO_APPS+PROJECT_APPS+PACKAGED_APPS

#----------------------------------------------------------------
# install widget-tweaks with : pip install django-widget-tweaks
# see : https://github.com/jazzband/django-widget-tweaks
#----------------------------------------------------------------


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'account.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'flowka.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('apps/templates'),root('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'core.context_processors.site',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'account.User'


USE_THOUSAND_SEPARATOR=True

TIME_ZONE = 'Europe/Paris'

USE_TZ = True

APPEND_SLASH=True

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_EXEMPT_URLS=(
    '/account/logout/',
    '/account/signup/',
    '/home/home/',
    '/home/parameters/',
    '/home/slider/',
    '/home/legal/',
    '/home/privacy/',
    '/home/overview/',
    '/home/',
    '/contact/',
    '/account/password_reset/',
    '/account/password_reset_done/',
    '/account/password_reset_confirm/',
    '/datacollect/rest/dataset/',
    '/datacollect/rest/transform/',
    '/datacollect/rest_column/',
    '/filer/rest/file/error/',
    '/survey/',
    '/survey/survey/',
    '/survey/2019/',
    )

#----------------------------------------------------
#STORAGE#

#DEFAULT_FILE_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'
# SFTP_STORAGE_HOST = get_secret("SFTP_STORAGE_HOST")
# SFTP_STORAGE_ROOT = get_secret("SFTP_STORAGE_ROOT")
# SFTP_STORAGE_PARAMS = {
#     'password' : get_secret("SFTP_STORAGE_PASSWORD"),
#     'username' : get_secret("SFTP_STORAGE_USERNAME"),
#     'port' : get_secret("SFTP_STORAGE_PORT"),
#     }
# SFTP_STORAGE_INTERACTIVE = False


#-----------------------------------------------------
import re
IGNORABLE_404_URLS = (
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)


#----------------------------------------------------
#
#   CITIES
#
#CITIES_CONTINENT_MODEL=cities.Continent
#CITIES_COUNTRY_MODEL=cities.Country
#CITIES_CITY_MODEL=cities.City
#----------------------------------------------------

#----------------------------------------------------
#
#   INTERNATIONALIZATION
#
# python manage.py makemessages -l en   # generate a .po file for english
# python manage.py makemessages --all    # update all .po files
# python manage.py compilemessages        # compile all messages from .po to .mo
#
# https://docs.djangoproject.com/en/2.0/topics/i18n/
#

USE_I18N = True
USE_L10N = True

gettext = lambda x: x

LANGUAGES = (
   ('fr', gettext('French')),
   ('en', gettext('English')),
)

LANGUAGE_CODE = 'en'


LOCALE_PATHS = (
root('locale'),
)

LANGUAGE_COOKIE_AGE =60*60*24*30*3
LANGUAGE_COOKIE_NAME = 'flowka_language'

#----------------------------------------------------
#                 FILER
FILER_IS_PUBLIC_DEFAULT=False

#----------------------------------------------------
#                 RABBITMQ

#----------------------------------------------------
#                 TAGULOUS

TAGULOUS_AUTOCOMPLETE_JS = (
    'tagulous/lib/jquery.js',
    'tagulous/lib/select2-3/select2.min.js',
    'tagulous/tagulous.js',
    'tagulous/adaptor/select2.js',
)

TAGULOUS_AUTOCOMPLETE_CSS = {
    'all': ['tagulous/lib/select2-3/select2.css']
}
SERIALIZATION_MODULES = {
    'xml':    'tagulous.serializers.xml_serializer',
    'json':   'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml':   'tagulous.serializers.pyyaml',
}


#-----------------------------------------------
# MESSAGES
#-------------------------------------------------

MESSAGE_TAGS = {
    0: 'tiny',
    10: 'debug',
    12: 'process',
    15: 'mail',
    20: 'info',
    25: 'success',
    30: 'warning',
    40: 'error',
    50: 'critical'
}

#------------------------ AWS ---------
AWS_DEFAULT_ACL = None
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_S3_USER=get_secret('AWS_S3_USER')
AWS_STORAGE_BUCKET_NAME = 'ilgigrad-staging-bucket'
AWS_S3_URL = 'https://{0}.s3-website.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
AWS_S3_OBJECT_PARAMETERS = {'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT','CacheControl': 'max-age=86400000',}
AWS_STATIC_DIR='static/'
AWS_LOCATION='uploads'
AWS_MEDIA_DIR='uploads/'
AWS_S3_REGION_NAME='eu-west-3'