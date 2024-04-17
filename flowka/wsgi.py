"""
WSGI config for flowka project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

#site.addsitedir('/home/david/PythonEnv/djangoflowkaenv/lib/python3.6/site-packages')

sys.path.append('/home/david/DjangoProjects/flowkaenv/lib/python3.6/site-packages')
sys.path.append('/home/david/DjangoProjects/flowka')
sys.path.append('/home/david/DjangoProjects/flowka/flowka')


os.environ["DJANGO_SETTINGS_MODULE"]="flowka.staging_settings"
#----------------------------------------------------

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    #from whitenoise import WhiteNoise
    #application = WhiteNoise(application,root='/static/')
except Exception:
    # Error loading applications
    print('error get wsgi_appligation in wsgi.py')
