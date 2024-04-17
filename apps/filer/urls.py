from django.conf.urls import url
from filer.views import (
    FileListView,
    PhotoListView,
    DataFileListView,
    FileLoadView,
    FileDownloadView,
    FileDeleteView,
    FileRemoveView,
    FileAddToFolderView,
    FileAddTagsView,
    FileRemoveTagsView,
    FileCopyView,
    )
from filer.folder_views import (
        FolderCreateView,
        FolderDeleteView,
        FolderUpdateView,
        )

from filer.rest_views import DataFileRestView

app_name = 'filer'

urlpatterns = [
    url(r'^photo/list/(?P<folderid>[0-9]+)?/(?P<uid>[0-9a-f\-]{36})?$',PhotoListView.as_view(),name='photo_list'),
    url(r'^datafile/list/(?P<folderid>[0-9]+)?/(?P<uid>[0-9a-f\-]{36})?$',DataFileListView.as_view(),name='datafile_list'),
    url(r'^file/list/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileListView.as_view(),name='file_list'),
    url(r'^file/list/$',FileListView.as_view(),name='file_list'),
    url(r'^file/load/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileLoadView.as_view(),name='file_load'),
    url(r'^file/download/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileDownloadView.as_view(),name='file_download'),
    url(r'^file/delete/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileDeleteView.as_view(),name='file_delete'),
    url(r'^file/remove/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileRemoveView.as_view(),name='file_remove'),
    url(r'^file/tofolder/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileAddToFolderView.as_view(),name='file_addtofolder'),
    url(r'^file/addtags/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileAddTagsView.as_view(),name='file_addtags'),
    url(r'^file/removetags/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileRemoveTagsView.as_view(),name='file_removetags'),
    url(r'^file/copy/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FileCopyView.as_view(),name='file_copy'),
    url(r'^folder/create/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FolderCreateView.as_view(),name='folder_create'),
    url(r'^folder/update/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w*:\w+)$',FolderUpdateView.as_view(),name='folder_update'),
    url(r'^folder/delete/(?P<folderid>[0-9]+)/(?P<uid>[0-9a-f\-]{36})/(?P<next>\w+:\w+)$',FolderDeleteView.as_view(),name='folder_delete'),
    url(r'^rest/file/error/(?P<uid>[0-9a-f\-]{36})$',DataFileRestView.as_view(),name='file_rest_error'),
]
