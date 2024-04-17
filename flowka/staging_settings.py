from .base_settings import *
#----------------------------------------------------------------
# SECURITY WARNING: don't run with debug turned on in production!
#----------------------------------------------------------------
DEBUG = False
#------------------------------------------------------------------------
# from django.contrib.sites.models import Site
# site,created=Site.objects.get_or_create(name='flowka.com')
# SITE_ID=site.id

ALLOWED_HOSTS = [
    'ilgigrad.net',
    'ilgigrad.fr',
    'ilgigrad.com',
    'flowka.com',
    'flowka.net',
    'flowka.fr',
    'www.flowka.fr',
    'www.flowka.net',
    'www.flowka.com',
    'www.ilgigrad.fr',
    'www.ilgigrad.com',
    'www.ilgigrad.net',
    '92.flowka.com',
    '92.flowka.net',
    '92.flowka.fr',
    '92.ilgigrad.fr',
    '92.ilgigrad.com',
    '92.ilgigrad.net',
    '127.0.0.1',
    '176.160.139.22',
    'localhost',
    ]

SITE_URL='https://92.ilgigrad.net'
#FORCE_SCRIPT_NAME = '/flowka'

# Application definition

#INSTALLED_APPS += ['mod_wsgi.server',]

MIDDLEWARE += [
#    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

PACKAGED_APPS+=['storages',]


WSGI_APPLICATION = 'flowka.wsgi.application'

    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#----------------------------------------------------
EMAIL_HOST_USER=get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=get_secret('EMAIL_HOST_PASSWORD')
EMAIL_HOST='smtpauth.online.net'
EMAIL_PORT='587'
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL='noreply@flowka.com'


STATIC_URL = '/static/'

#------------------ AWS S3 ---------------------
#https://650153547647.signin.aws.amazon.com/console
#BUCKET ARN: aws:s3:::ilgigrad-staging-bucket
#http://ilgigrad-staging-bucket.s3-website.eu-west-3.amazonaws.com
#-------------------------------------------------------------

MEDIA_URL=AWS_S3_URL + AWS_MEDIA_DIR
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


#----------------------------------------------------------------------------
#'http://ilgigrad-staging-bucket.s3-website.eu-west-3.amazonaws.com/uploads/'
#AWS_MEDIA_LOCATION = 'uploads'
#AWS_STATIC_LOCATION = 'static'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#https://650153547647.signin.aws.amazon.com/console
#BUCKET ARN: aws:s3:::ilgigrad-staging-bucket
#http://ilgigrad-staging-bucket.s3-website.eu-west-3.amazonaws.com

#AWS_STATIC_LOCATION = 'static'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db336842_flowkastaging2',
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
        'HOST': 'db336842-flowkastaging2.sql-pro.online.net',
        'PORT': '5432',
        'ATOMIC_REQUESTS':False,
        }
    }

RABBITMQ={
    'USER':get_secret('RABBITMQ-USER'),
    'PASSWORD':get_secret('RABBITMQ-PASSWORD'),
    'VHOST':'fl02',
    'SERVER':'rabbit.75.ilgigrad.net',
    'PORT':'5672',
    'QUEUE':'DC'}
