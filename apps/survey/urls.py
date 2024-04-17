from django.conf.urls import url
from . import views # import views so we can use them in urls.

app_name = 'survey'

urlpatterns = [
    url(r'^$', views.SurveyView.as_view(), name='survey'),
    url(r'^2019/$', views.Survey2019View.as_view(), name='survey2019'),
]
