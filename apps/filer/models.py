from django.db import models
from django.utils.translation import ugettext_lazy as _
import hashlib
from django.conf import settings
from enum import Enum
from filer.managers import FileManager, FolderManager
from tagulous.models import TagField
from tag.models import TagSubject
from uuid import uuid1


import datetime

from core.utils import size_prefix,shortdate
from core.mixins import EnumMixin

from core.custom_models_fields import ColorField
from account.perms import PermMixin
from account.mixins import OwnerMixin
from core.utils import Const, PathAndRename



def is_public_default():
    return settings.FILER_IS_PUBLIC_DEFAULT


class AbstractFile(models.Model):
    class FILE_STATUS(EnumMixin,Enum):
        undef   = (0,'undefined')
        unload  = (1,'unload')
        load    = (2,'loaded')
        clean   = (3,'cleaned')
        learn   = (4,'learned')
        predict = (5,'predicted')


    class FILE_TYPE(EnumMixin,Enum):
        img  = (1,'img')
        file = (2,'file')
        xls  = (3,'xls')
        json = (4,'json')
        xml  = (5,'xml')
        csv  = (6,'csv')
        txt  = (7,'txt')
        html = (8,'html')
        void = (9,'void')


    uid = models.CharField(max_length=36,null=True, blank=True, unique=True)
    file = models.FileField(_('file'), null=True, blank=True, max_length=255, upload_to=PathAndRename())
    original_filename = models.CharField(_('original filename'), default=None, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255,default='', blank=True, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)
    _sha1 = models.CharField(_('sha1'),max_length=40, blank=True, default='')
    _status = models.IntegerField(_('status'), default=FILE_STATUS.get_value('undef'),choices=[x.value for x in FILE_STATUS])
    _type = models.IntegerField(_('type'), null=True, default=FILE_TYPE.get_value('void') ,choices=[x.value for x in FILE_TYPE])
    _file_data_changed_flag=None
    _file_size = models.BigIntegerField(_('file size'), null=True, blank=True)
    is_valid = models.BooleanField(_('is valid'), default=True)
    is_public = models.BooleanField(default=is_public_default(), verbose_name=_('Permissions disabled'))
    is_favorite=models.BooleanField(_('favorite'), default=False)
    subjects = TagField(to=TagSubject)


    objects = FileManager()

    class Meta:
        abstract = True
        verbose_name = 'file'
        verbose_name_plural = 'files'

    def url(self):
        return self.file.url

    def __init__(self, *args, **kwargs):

        super(AbstractFile,self).__init__(*args,**kwargs)
        self.file_data_changed(post_init=True)


    def delete(self, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        super(AbstractFile,self).delete(*args,**kwargs)
        if self.__class__==AbstractFile:
            pass
        elif issubclass(self.__class__, AbstractFile):
            if not self.__class__.objects.filter(file=self.file.name).exists():
                self.file.delete(False)

    def file_data_changed(self, post_init=False):
        #import ipdb; ipdb.set_trace()
        if post_init and self._file_size and self._sha1!='':
            #case init from database load
            return False
        else:
            #case init new filer object
            if self.uid is None:
                self.uid=str(uuid1())
            try:
                self._file_size=self.file.size
            except:
                self._file_size=None

            try:
                #import ipdb; ipdb.set_trace()
                self.generate_sha1()
            except Exception:
                self._sha1=''

            if  self.original_filename is None :
                self.original_filename=self.file.name
                self.name=self.original_filename
                self.file_type()




    def generate_sha1(self):
        sha=hashlib.sha1()
        self.file.seek(0)
        while True:
            buf=self.file.read(104857600)
            if not buf:
                break
            sha.update(buf)
        self._sha1=sha.hexdigest()
        self.file.seek(0)

    @property
    def shortname(self):
        return(self.name.split('.')[0])

    @property
    def shortuploaded_at(self):
        return shortdate(self.uploaded_at)

    @property
    def shortmodified_at(self):
        return shortdate(self.modified_at)

    @property
    def modified_today(self):
        return isinstance(shortdate(self.modified_at),datetime.time)

    @property
    def uploaded_today(self):
        return isinstance(shortdate(self.uploaded_at),datetime.time)

    @property
    def size(self):
        return self._file_size

    @property
    def p_size(self):
        return size_prefix(self._file_size,precision=1,bytes=True,short=True)

    @property
    def name_description(self):
        if self.description:
            return "{name}: {desc}".format(**{'name':self.original_filename, 'desc':self.description})
        return "{name}".format(**{'name':self.original_filename})

    @property
    def sha1(self):
        return(self._sha1)


    @property
    def url(self):
        try:
            return self.file.url
        except:
            return ""

    @property
    def path(self):
        try:
            return self.file.path
        except:
            return ""


    def get_status(self):
        return self.get__status_display()

    def set_status(self, status):
        self._status=status

    status = property(get_status,set_status)

    @property
    def status_icon(self):
        if not self.is_valid:
            return Const.ICON["c-invalid"]
        icons=[
            Const.ICON["c-question"],Const.ICON["c-empty"],Const.ICON["c-down"],Const.ICON["c-plus"],
            Const.ICON["c-play"],Const.ICON["c-check"]]
        return icons[self._status]

    @property
    def has_alert(self):
        if self.is_valid and self._status>self.FILE_STATUS.get_value('unload'):
            return False
        return True

    @property
    def status_ext(self):
        if self.is_valid:
            return self.get__status_display()
        return '{} {} {}'.format(_('invalid'),_('and'),self.get__status_display())

    @property
    def type(self):
        return self.get__type_display()

    @property
    def type_color(self):
        colors=[
        "fl-bg-white fl-txt-prune",#file
        "fl-bg-black fl-txt-white",#img
        "fl-bg-light fl-txt-prune",#file
        "fl-bg-anis fl-txt-white",#xls
        "fl-bg-rose fl-txt-white",#json
        "fl-bg-dark fl-txt-white",#xml
        "fl-bg-apricot fl-txt-white",#csv
        "fl-bg-electric fl-txt-white",#txt
        "fl-bg-prune fl-txt-white",#html
        "fl-bg-white fl-txt-dark",]#void
        return colors[self._type]

    @property
    def type_icon(self):
        icons=[
        "fal fa-file",#file
        "fal fa-file-image",#img
        "fal fa-file",#file
        "fal fa-file-excel",#xls
        "fal fa-file-spreadsheet",#json
        "fal fa-file-spreadsheet",#xml
        "fal fa-file-csv",#csv
        "fal fa-file-alt",#txt
        "fal fa-file-code",#html
        "",]#void
        return icons[self._type]



    @property
    def duplicates(self):
        return AbstractFile.objects.find_duplicates(self)

    @property
    def short_name(self):
        if len(self.name)>25:
            ext=self.name.split('.')[-1]
            main=self.name.split('.')[0]
            prefix=main[:15]
            suffix=main[-5:]
            return prefix+'...'+suffix+'.'+ext
        else:
            return self.name

    def save(self, **kwargs):

        self.file_data_changed()
        if self.__class__==AbstractFile:
            pass
        elif issubclass(self.__class__, AbstractFile):
            self._type_plugin_name=self.__class__.__name__
        #import ipdb; ipdb.set_trace()
        if self.is_favorite:
            self.owner.myfavs.file.add(self)
        elif self.owner:
            self.owner.myfavs.file.remove(self)

        super(AbstractFile, self).save( **kwargs)

    save.alters_data=True



    def file_type(self):
        UNDEF_FILE=self.FILE_TYPE.get_value('file')
        try:
            ext = self.original_filename.lower().split('.')[-1]
            if ext in ['xls','xlsx']:
                ext='xls'
            elif ext in ['htm','html']:
                ext='html'
            elif ext in ['png','jpg','jpeg','gif']:
                ext='img'
            self._type=self.FILE_TYPE.get_value(ext) or UNDEF_FILE
        except:
            self._type = UNDEF_FILE
        return self._type

    def __str__(self):
        return "id:%s | %s | %s | %s " % (
            str(self.id),
            self.type,
            self.status,
            self.name,
        )

class File(PermMixin,OwnerMixin,AbstractFile):
    pass
    class Meta:
        verbose_name = 'data file'
        verbose_name_plural = 'data files'

class Folder(PermMixin,OwnerMixin,models.Model):
    uid = models.CharField(max_length=36, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255,default='', blank=True, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description'))
    icon = models.CharField(max_length=50,default='', blank=True, verbose_name=_('icon'))
    color = ColorField(max_length=7,default='#EEEEEE', verbose_name=_('color'))
    parent =  models.ForeignKey('self', on_delete=models.CASCADE,related_name='children', verbose_name=_('parent folder'), null=True)
    is_public = models.BooleanField(default=False, verbose_name=_('is public'))
    is_root = models.BooleanField(default=False, verbose_name=_('root folder'))
    file = models.ManyToManyField(File,
            verbose_name=_('files in folder'),
            blank=True,
            help_text=_('file in folders'),
            related_name="%(app_label)s_%(class)s_related",
            related_query_name="%(app_label)s_%(class)ss",
            )
    objects=FolderManager()

    class Meta:
        verbose_name = 'folder'
        verbose_name_plural = 'folders'

    def __init__(self, *args, **kwargs):
        super(Folder,self).__init__(*args,**kwargs)
        if self.uid is None or self.uid=='':
            self.uid=str(uuid1())

    def __str__(self):

        if self.parent is None:
            parent=''
        else:
             parent=self.parent_id
        return "id:%s | %s | %s" % (
            str(self.id),
            self.name,
            parent,
        )

import filer.signals
