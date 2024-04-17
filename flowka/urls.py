"""flowka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from store import views as storeviews
from account import views as accountviews
from message import views as messageviews
from home import views as homeviews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [

    url(r'^adminfl/', admin.site.urls),
    url(r'^$', homeviews.home, name='home'),
    url(r'^store/', include('store.urls', namespace='store')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^contact/$',storeviews.contact,name='contact'),
    url(r'^filer/',include('filer.urls', namespace='filer')),
    url(r'^message/',include('message.urls', namespace='message')),
    url(r'^survey/',include('survey.urls', namespace='survey')),
    #url(r'^tag/',include('tag.urls', namespace='tag')),
    #url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^tag/', include('tag.urls', namespace='tag')),
    url(r'^datacollect/',include('datacollect.urls', namespace='datacollect')),
    url(r'^rabbitMQ/',include('rabbitMQ.urls', namespace='rabbitMQ')),]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
