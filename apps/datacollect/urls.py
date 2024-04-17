from django.conf.urls import url
from . import views as dc_views
from . import rest_views as ds_rest_views
from .columns import rest_views as col_rest_views
from .columns import views as col_views


app_name = 'datacollect'

urlpatterns = [
    url(r'^meta/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',dc_views.MetaEditView.as_view(),name='meta'),
    url(r'^snippet/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',dc_views.SnippetEditView.as_view(),name='snippet'),
    url(r'^clean/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',dc_views.DataCleanView.as_view(),name='clean'),
    url(r'^column/(?P<uid>[0-9a-f\-]{36})/(?P<columnid>[0-9]+)$',col_views.ColumnView.as_view(),name='column'),
    url(r'^timecolumn/(?P<uid>[0-9a-f\-]{36})/(?P<columnid>[0-9]+)$',col_views.TimeColumnView.as_view(),name='timecolumn'),
    url(r'^splitcolumn/(?P<uid>[0-9a-f\-]{36})/(?P<columnid>[0-9]+)$',col_views.SplitColumnView.as_view(),name='splitcolumn'),
    url(r'^substrcolumn/(?P<uid>[0-9a-f\-]{36})/(?P<columnid>[0-9]+)$',col_views.SubstrColumnView.as_view(),name='substrcolumn'),
    url(r'^regexcolumn/(?P<uid>[0-9a-f\-]{36})/(?P<columnid>[0-9]+)$',col_views.RegexColumnView.as_view(),name='regexcolumn'),
    url(r'^rest/dataset/(?P<uid>[0-9a-f\-]{36})$',ds_rest_views.DataSetRestView.as_view(),name='rest_dataset'),
    #url(r'^dataset$',dc_views.DataSetView.as_view(),name='dataset'),
    url(r'^rest/transform/(?P<uid>[0-9a-f\-]{36})$',ds_rest_views.TransformRestView.as_view(),name='rest_transform'),
    url(r'^rest_column/(?P<uid>[0-9a-f\-]{36})/(?P<columnid>[0-9]+)$',col_rest_views.ColumnRestView.as_view(),name='rest_column'),
]

#/(?P<uid>[0-9a-f\-]{36})/(?P<columnid>[0-9a-f\_\-]*)"
