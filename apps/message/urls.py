from django.conf.urls import url
from message.views import MessageListSerializer
#from message.views MessageListView
app_name = 'message'

urlpatterns = [
    # url(r'^list/$',MessageListView.as_view(),name='message_list'),
    url(r'^rest_list/$',MessageListSerializer.as_view(),name='message_list_rest'),
]
