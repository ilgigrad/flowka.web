from django.conf.urls import url
from . import views
app_name = 'home'

urlpatterns = [
    url(r'^private/$', views.private, name='private'),
    url(r'^hello/$', views.hello, name='hello'),
    url(r'^message/$', views.hello, name='message'),
    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^slider/$', views.slider, name='slider'),
    url(r'^parameters/$', views.ParametersView.as_view(), name='parameters'),
    url(r'^next/$', views.next, name='next'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^legal/$', views.legal, name='legal'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^support/$', views.support, name='support'),
    url(r'^error/(?P<errid>[0-9]+)$',views.error_page,name='error'),
]
