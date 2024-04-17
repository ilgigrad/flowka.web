from django.conf.urls import url
from . import views # import views so we can use them in urls.

app_name = 'store'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<fee_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^pricing/$', views.pricing, name='pricing'),
    url(r'^search/$', views.search, name='search'),
    url(r'^listing/$', views.listing, name='listing'),
    url(r'^contact/$',views.contact,name='contact'),
]