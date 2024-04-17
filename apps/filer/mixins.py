from django.db import models
from filer.models import File,Folder
from django.shortcuts import get_object_or_404

class AvatarMixin(models.Model): #if mixin inherits from models.model, then class can't inherit from models.Model
    photo = models.ForeignKey(File, null=True, on_delete=models.SET_NULL,related_name='%(app_label)s_%(class)s_avatar')
    class Meta(): #not really a mixin but an abstract class...
        abstract=True

    def set_avatar(self,photo):
        oldphoto=self.photo
        self.photo=photo
        self.save()
        if oldphoto:
            oldphoto.delete()
        return self.photo

    def get_avatar(self):
        return self.photo

    avatar= property(get_avatar,set_avatar)


    @property
    def avatar_url(self):
        if self.photo:
            url= self.photo.url
        else:
            url= '/static/pictures/unknown.jpg'
        return url

    def avatar_html (self):
        return mark_safe('<img src="{}" width="200" height="200">'.format(self.avatar_url()))

    def save(self, *args,**kwargs):
        #import ipdb; ipdb.set_trace()
        self.website=(self.website or '').lower()
        super(AvatarMixin, self).save(*args,**kwargs)


class FolderViewMixin():
    class Meta():
        abstract=True
    def __init__(self):
        self.folders=[]
        self.folderId=None
        self.folderName=''

    def load_session(self,request):
        if hasattr(request,'session'):
            self.folders=request.session.get('folders',self.folders)
            self.folderId=request.session.get('folderId',self.folderId)
            self.folderName=request.session.get('folderName',self.folderName)

    def get(self,request):
        self.load_session(request)
        folderId=request.GET.get("folderId",None)
        if folderId: #click on a folder
            self.folderId=int(folderId)
            folder=get_object_or_404(Folder,pk=self.folderId)
            self.folderName=folder.name
            folders=Folder.objects.current_folders(request.user,folder=self.folderId)
            self.folders=[
                {'id':x.id,'name':x.name,'color':x.color,'icon':x.icon}
                for x in folders
                ]
        elif self.folderId is None: #first load
            #import ipdb; ipdb.set_trace()
            folders=Folder.objects.current_folders(request.user,self.folderId)
            self.folders=[
                {'id':x.id,'name':x.name,'color':x.color,'icon':x.icon}
                for x in folders
                ]
            self.folderId=self.folders[0]['id']
            self.folderName=self.folders[0]['name']

        request.session['folders']=self.folders
        request.session['folderId']=self.folderId
        request.session['folderName']=self.folderName
        return
