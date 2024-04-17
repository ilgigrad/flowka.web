from django.conf.urls import url
from . import views as mq_views


app_name = 'rabitMQ'

urlpatterns = [
    url(r'^receive/$',mq_views.receive,name='receive'),
    url(r'^send(?P<body>.*)/$',mq_views.send,name='send'),
]
