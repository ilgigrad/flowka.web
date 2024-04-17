from django.db import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404
from core.utils import Const,PathAndRename
from django.core.files.storage import default_storage
from django.conf import settings
import re

class FileManager (models.Manager):

    def find_all_duplicates(self):
        r = {}
        for file_obj in self.all():
            if file_obj.sha1:
                q=self.filter(sha1=file_obj.sha1)
                if len(q)>1:
                    r[file_obj.sha1]=q
        return r

    def find_duplicates(self, file_obj):
        return [i for i in self.exclude(pk=file.obj.pk).filter(sha1=file_obj.sha1)]

    def authorized_from_folder(self, user, folder, perm):

            query=self.filter(filer_folders=folder)
            query_public=query.filter(is_public=True)
            if user.is_authenticated:
                query_hasperm=query.filter(perms__holder=user.holder,
                perms__perm_label='can_list')
                query= query_public | query_hasperm
            else:
                query = query_public
            return query

    def purge_invalid(self):
        self.filter(is_valid=False).delete()

    def copy(self,obj):
        newfilename=PathAndRename().__call__(obj,obj.file.name)
        #import ipdb; ipdb.set_trace()
        binList=['img']
        b=['','+b'][obj.type in binList]
        src=default_storage.open(obj.file.name,"r"+b)
        name=''.join(obj.name.split('.')[:-1])+'-cpy'+'.'+obj.name.split('.')[-1]
        new=self.create(name=name, file=src) # works with minio and SFTP and to test with local storage
        # if above do not work with other cases than minio; uncomment block below
        # if re.search(r'minio', settings.DEFAULT_FILE_STORAGE):
        #     new=self.create(name=name, file=src)
        # else:
        #     dest=default_storage.open(newfilename,"w"+b+"+")
        #     for chunk in src.chunks():
        #         dest.write(chunk)
        #     new=self.create(name=name, file=dest)
        #     dest.close()
        src.close()
        new.name=name
        new.original_filename=obj.original_filename
        new.status=new.FILE_STATUS.get_value('load')
        new.generate_sha1()
        new.save()
        return new


class FolderManager(models.Manager):

    def myfolders(self,user):
        """ folder that user can read
        """
        queryMyPerms  = self.filter(
            perms__holder=user.holder,
            perms__perm_label='can_read')
        return queryMyPerms

    def roots(self,user):
        """ 3 main root folders : my files / favorites / shared
        """
        if user.is_authenticated:
            return self.prefetch_related('perms').filter(
                perms__holder=user.holder,
                perms__perm_label='can_read',
                owner=user,
                is_root=True,
                parent=None,
                is_public=False)
        else:
            return self.filter(id=0)

    def myfiles(self,user):
        """user root folder : myfiles
        """
        return self.roots(user).get(name="all my files",is_root=True)

    def myfavs(self,user):
        """user root folder : myfavs
        """
        return self.roots(user).get(name="favorites",is_root=True)

    def childs(self,folder):
        """child of a folder
        """
        return self.filter(parent=folder)



    def get_folders_from_id(self,folderid,uid,user):
        """
        return a directory of folders from a folder it
        contains :
        current folder,
        parent folder,
        child folders
        and roots folders ("all my files"/shared/favorites)
        """
        if folderid is not None and (uid!='' or uid is None): #click on a folder
            folder=self.prefetch_related('perms').get(pk=int(folderid),uid=uid)
        else:
            folder=self.myfiles(user)
        current={
            'id':folder.id,
            'uid':folder.uid,
            'name':folder.name,
            'description':folder.description,
            'can_add':['disabled','enabled'][folder.has_perm(user.holder,'can_add')],
            'can_edit':['disabled','enabled'][folder.has_perm(user.holder,'can_edit')],
            'can_delete':['disabled','enabled'][folder.has_perm(user.holder,'can_delete')],
            }

        childs=self.childs(folder=folder.id)
        childs=[{
            'id':x.id,
            'uid':x.uid,
            'name':x.name,
            'deletable':x.has_perm(user.holder,'can_delete'),
            'color':x.color,
            'icon':x.icon,
            }
            for x in childs]
        roots=self.roots(user)
        roots=[{
            'id':x.id,
            'uid':x.uid,
            'name':x.name,
            'color':x.color,
            'icon':x.icon,
            'deletable':False
            }
            for x in roots
            ]
        if folder.parent:
            parent={
                'id':folder.parent.id,
                'uid':folder.parent.uid,
                'name':folder.parent.name,
                'color':Const.COLOR['apricot'],
                'icon':Const.ICON['back']
                }
        else:
            parent=None
        return {'current':current,'childs':childs,'roots':roots,'parent':parent}
