
from .base_settings import *


#------------------------------------------------------------------------
DEBUG = True
#------------------------------------------------------------------------
# from django.contrib.sites.models import Site
# site,created=Site.objects.get_or_create(name='ilgigrad.net')
# SITE_ID=site.id

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INSTALLED_APPS += ['debug_toolbar',]

PACKAGED_APPS+=['minio_storage',]


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: True,  # disables it
    # '...
}

###### ACTIVATE ABOVE FOR TESTING AWS AND DEACTIVATE CURRENT DEFAULT_FILE_STORAGE###
#MEDIA_URL=AWS_S3_URL + AWS_MEDIA_DIR
#DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
DEFAULT_FILE_STORAGE = 'minio_storage.storage.MinioMediaStorage'
#####################################################################################

MINIO_STORAGE_ACCESS_KEY = get_secret("MINIO_STORAGE_ACCESS_KEY")
MINIO_STORAGE_SECRET_KEY = get_secret("MINIO_STORAGE_SECRET_KEY")
MINIO_STORAGE_ENDPOINT = 'minio.75.ilgigrad.net:9001'
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'uploads'
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_USE_HTTPS = False
MINIO_STORAGE_MEDIA_URL = 'http://minio.75.ilgigrad.net:80/uploads'
#MINIO_STORAGE_STATIC_BUCKET_NAME = 'static'
#STATICFILES_STORAGE = 'minio_storage.storage.MinioStaticStorage'
#MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
#MINIO_STORAGE_STATIC_URL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db15800_ilgigrad',
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
        'HOST': 'db15800-ilgigrad.sql-pro.online.net',
        'PORT': '5432',
        'ATOMIC_REQUESTS':False,
    }
}

#----------------------------------------------------
#   EMAIL
#
EMAIL_HOST='smtpauth.online.net'
EMAIL_PORT='2525'
EMAIL_HOST_USER=get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=get_secret('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL='noreply@ilgigrad.net'
#----------------------------------------------------

#-------------- ACTIVATE FOR LOCAL MAIL SERVER ---------------
#local server :
#host=localhost port=1025
#python -m smtpd -n -c DebuggingServer localhost:1025
# EMAIL_HOST='localhost'
# EMAIL_PORT='1025'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/django'




#-------------- ACTIVATE FOR SFTP STORAGE ---------------
#DEFAULT_FILE_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'
# SFTP_STORAGE_HOST = 'django.75.ilgigrad.net'
# SFTP_STORAGE_ROOT = '/uploads/'
# SFTP_STORAGE_PARAMS = {
#     'password' : get_secret("SFTP_STORAGE_PASSWORD"),
#     'username' : get_secret("SFTP_STORAGE_USERNAME"),
#     'port' : '2202',
#     }
#
# SFTP_STORAGE_INTERACTIVE = False
#MEDIA_URL = '/uploads/'
#STATIC_URL = '/static/'


#-------------- ACTIVATE FOR SQL LITE DATABASE ---------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'flowkalocal.db',
#         'ATOMIC_REQUESTS':False,
#     }
# }

RABBITMQ={
    'USER':get_secret('RABBITMQ-USER'),
    'PASSWORD':get_secret('RABBITMQ-PASSWORD'),
    'VHOST':'fl01',
    'SERVER':'rabbit.75.ilgigrad.net',
    'PORT':'5672',
    'QUEUE':'DC'}
