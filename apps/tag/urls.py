from django.conf.urls import url
from . import views as tag_views
import tagulous.views
from .models  import TagSubject


app_name = 'tag'

urlpatterns = [
    url(
        r'^tags/$',
        tagulous.views.autocomplete,
        {'tag_model': TagSubject},
        name='tag_subject_autocomplete',
    ),
    url(r'^tags/search/(?P<next>\w*:\w*)$',tag_views.SearchTagView.as_view(),name='tag_search'),
]
