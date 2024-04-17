from django.shortcuts import  redirect,get_object_or_404
from django.template.response import TemplateResponse, HttpResponse
from core.utils import paginator,get_form_errors_list,get_session
from django.views.generic import View
from django.contrib import messages
from message.models import Message
from django.utils.translation import ugettext as _
from rabbitMQ.send import mqsend




from filer.models import File
from filer.folder_views import FolderView,SortView,FolderUpdateView,FolderCreateView,FolderDeleteView
from filer.models import Folder
from filer.forms import DataFileForm,CropForm
from tag.views import SearchTagView,AddTagView

from tag.models import search_by_tags
from django.views.decorators.csrf import csrf_exempt



class PictView():
    pictDict={'st':(28,120),'sm':(91,60),'xs':(299,30)} #picture-viewer will display 28 - 91 - 299 pictures in a page before scrolling
    def get(self,request):
        context=get_session(request,'context')
        pictDim=context.get('pictDim','st')
        pictDim=request.GET.get('pictDim',pictDim)
        context['pictDim']=pictDim
        #context['filesPerPage']=self.pictDict[pictDim][0]
        context['filesPerPage']=500
        context['pictSize']=self.pictDict[pictDim][1]
        request.session['context']=context
        return context['filesPerPage']


class PhotoListView(View):
    def get(self,request,folderid=None,uid=None):

        if folderid is None:
            sessionContext=get_session(request,'context')
            try:
                folderid=sessionContext['folders']['current']['id']
                uid=sessionContext['folders']['current']['uid']
            except:
                folderid=0
                uid=''
        next='filer:photo_list'
        return redirect('filer:file_list',next=next,folderid=folderid, uid=uid)

class DataFileListView(View):
    def get(self,request,folderid=None,uid=None):
        if folderid is None:
            sessionContext=get_session(request,'context')
            try:
                folderid=sessionContext['folders']['current']['id']
                uid=sessionContext['folders']['current']['uid']
            except:
                folderid=0
                uid=''
        next='filer:datafile_list'
        return redirect('filer:file_list',next=next,folderid=folderid, uid=uid)

class FileListView(View):

    def __init__(self,*args,**kwargs):
        super(FileListView,self).__init__(*args,**kwargs)
        pass


    def get(self,request,next='filer:file_list',folderid=0, uid=None):

        SortView().get(request)
        folderid,uid=FolderView().get(request,folderid,uid)
        folderupdate_form=FolderUpdateView().get(request,folderid,uid)
        foldercreate_form=FolderCreateView().get(request)
        #import ipdb; ipdb.set_trace()
        tags_form=SearchTagView().get(request)
        sessionContext=get_session(request,'context')
        files=search_by_tags(
            user=request.user,
            cls=File,
            column='subjects',
            strict=sessionContext['strict'],
            searchTags=sessionContext['searchTags'])

        import re
        match=re.search(r'photo',next)
        if match:
            filesPerPage=PictView().get(request)
            template='filer/photo_list.html'
            files=files.filter(_type=File.FILE_TYPE.get_value('img'))
        else:
            filesPerPage=100
            template='filer/datafile_list.html'
            if re.search(r'data',next): #onlydatafiles else data and images
                files=files.exclude(
                    _type=File.FILE_TYPE.get_value('img'))
            else:
                files=self.search(request)
                next='filer:datafile_list'

            if hasattr(File,sessionContext['order']):
                if sessionContext['direction']:
                    files=files.order_by(sessionContext['order'])
                else:
                    files=files.order_by('-{}'.format(sessionContext['order']))
            else:
                files=files.order_by('-id')

        files=files.filter(filer_folders__id=folderid, )
        page=request.GET.get('page')

        files, paginate = paginator(files,filesPerPage,page)
        from copy import deepcopy
        context=deepcopy(sessionContext)
        context.update({
        'files': files,
        'paginate': paginate,
        'page': page,
        'tags_form': tags_form,
        'foldercreate_form': foldercreate_form,
        'folderupdate_form': folderupdate_form,
        'next': next

        })
        #import ipdb; ipdb.set_trace()

        Message.objects.fetch(request)
        return TemplateResponse(request,template,context)
        #return HttpResponse('<html><body><h1>nothing</h1></body></html>')

    def search(self,request):
        query = request.GET.get('query')
        context=get_session(request,'context')
        if not query:
            query=context.get('query','')

        context['query']=query
        request.session['context']=context
        name = File.objects.filter(name__icontains=query)
        filename  = File.objects.filter(original_filename__icontains=query)
        owner = File.objects.filter(owner__last_name__icontains=query)
        tags =  File.objects.filter(subjects__label__icontains=query)
        description =  File.objects.filter(description__icontains=query)
        files= name | filename | owner | tags | description
        #then manage permissions
        public=files.filter(is_public=True).distinct()
        owner=files.filter(owner=request.user).distinct()
        perm=files.filter(perms__perm_label='can_list',perms__holder=request.user.holder).distinct()
        files= public | owner | perm
        files=files.distinct()
        return files

class FileLoadView(View):

    def post(self,request,folderid,uid,next):
        #import ipdb; ipdb.set_trace()
        import re
        match=re.search(r'photo',next)
        filelist=[]
        errors=[]
        nbfiles=1
        nberr=0
        files = request.FILES.getlist('file')
        nbfiles=len(files)
        if match: #file is an image
            form = CropForm(request.POST, request.FILES)
            loaded=True #images do not require additional process
        else: #datafile (csv/text/html/excel...)
            form = DataFileForm(request.POST, request.FILES)
            loaded=False #datafiles require additional process on ML server

        folder=get_object_or_404(Folder,id=folderid, uid=uid)

        if not form.is_valid():
            nberr=len(form.errors.get('file')) #count the errors (in case of multi files)

        if nbfiles-nberr>0: #assert one file is correct at least:
            filelist=form.save()


            for file in filelist: #addd some attributes to File object(s)
                file.owner=request.user
                file.is_public=False
                file.status=File.FILE_STATUS.get_value({False:'unload',True:'load'}[loaded])
                file.is_valid=True
                file.owner_perms(request.user.holder)
                file.save()
                if not loaded:
                    try:
                        mqsend(file.file.name,'DC',headers={'user-uid':request.user.uid,'user-id':request.user.id,'file-uid':file.uid,'file-id':file.id })
                    except:
                        messages.add_message(request, messages.INFO, "'{}' {}.".format(file.short_name,_('can not be processed for cleaning yet')))
                        file.save()

            request.user.myfiles.file.add(*filelist)
            if folder.has_perm(request.user.holder,'can_add'):
                folder.file.add(*filelist)

            if nbfiles>1:

                messages.add_message(request, messages.SUCCESS, "'{}' {}.".format(nbfiles-nberr,_('files have been succesfully uploaded')))
                if nberr>0:
                    messages.add_message(request, messages.WARNING, "'{}' {}.".format(nberr,_('files have not been uploaded')))
            else:
                messages.add_message(request, messages.SUCCESS, "'{}' {}.".format(filelist[0].short_name,_('has been succesfully uploaded')))

        for error in get_form_errors_list(form.errors):
            messages.add_message(request, messages.ERROR, error)

        return redirect(next, folderid=folderid, uid=uid)


class FileDeleteView(View):

    def post(self,request,folderid,uid,next):

        fileList=request.POST.get("fileList",'')
        if fileList!='' and isinstance(fileList,str):
            fileList= [s for s in fileList.split(",")]
        elif isinstance(fileList,int):
            fileList=[fileList]

        files=File.objects.filter(uid__in=fileList)
        for file in files:
                    if file.has_perm(request.user.holder,'can_delete'):
                        try:
                            file.delete()
                            messages.add_message(request, messages.SUCCESS, "'{}' {}.".format(file.short_name,_('has been deleted')))
                        except:
                            messages.add_message(request, messages.ERROR, "{} '{}'.".format(_('an error occured while deleting'),file.short_name))
                    else:
                        messages.add_message(request, messages.WARNING, "{} '{}'.".format(_('you have no permissions to delete.'),file.short_name))
        return redirect(next, folderid=folderid, uid=uid)


class FileRemoveView(View):

    def post(self,request,folderid,uid,next):

        fileList=request.POST.get("fileList",'')
        if fileList!='':
            fileList= [s for s in fileList.split(",")]

        files=File.objects.filter(uid__in=fileList)

        folder=get_object_or_404(Folder,id=folderid, uid=uid)
        for file in files:
            if file.is_public and folder==request.user.myfiles: #public file and in 'myfiles' folder, remove from all folders
                folders=request.user.myfolders.filter(file__id=file.id)
                file.filer_folder_related.remove(*folders)
                messages.add_message(request, messages.SUCCESS, "'{}' {}".format(file.short_name,_('succesfully removed from'),folder.name))
                messages.add_message(request, messages.SUCCESS, "'{}' {}".format(file.short_name,_('is public and has been also removed from all descending projects')))
            elif folder.has_perm(request.user.holder,'can_remove'):
                file.filer_folder_related.remove(folder)
                messages.add_message(request, messages.SUCCESS, "'{}' {}".format(file.short_name,_('succesfully removed from'),folder.name))
            else :
                messages.add_message(request, messages.WARNING, "{} '{}'. '{}' {}.".format(_('you have no permissions for removing objects from'),folder.name,file.short_name,_("has not been removed; try deletion instead.")))
        return redirect(next, folderid=folderid, uid=uid)


class FileAddToFolderView(View):

    def post(self,request,folderid,uid,next):

        folderList=request.POST.get("folderList",'')
        if folderList!='':
            folderList= [int(i) for i in folderList.split(",")]

        fileList=request.POST.get("fileList",'')
        if fileList!='':
            fileList= [s for s in fileList.split(",")]

        if len(folderList)>0 and len(fileList)>0:
            #folderList.append(folderid)
            folders=Folder.objects.filter(id__in=folderList)
            files=File.objects.filter(uid__in=fileList)
            for folder in folders:
                if folder.has_perm(request.user.holder,'can_add'):
                    folder.file.add(*files)
                    owner=Folder.objects.get(id=folderid).owner
                    if owner is None or owner!=request.user: #copy from another project add files to 'myfiles'
                        request.user.myfiles.file.add(*files)
                    addedFiles=', '.join([file.short_name for file in files])
                    messages.add_message(request, messages.SUCCESS, "{} {} '{}'".format(addedFiles,_('succesfully added to'),folder.name))
                else:
                    messages.add_message(request, messages.WARNING, "{} '{}'".format(_('you do not have perimission to add files to'),folder.name))
        else:
            messages.add_message(request, messages.ERROR, "{}".format(_('no project or no file selected')))
        return redirect(next, folderid=folderid, uid=uid)


class FileAddTagsView(View):

    def post(self,request,folderid,uid,next):
        #import ipdb; ipdb.set_trace()

        fileList=request.POST.get("fileList",'')
        if fileList!='':
            fileList= [s for s in fileList.split(",")]

        addtags=AddTagView().post(request)
        files=File.objects.filter(uid__in=fileList)
        if len(addtags)>0 and len(files)>0:
            for file in files:
                if file.has_perm(request.user.holder,'can_edit'):
                    try:
                        file.subjects.add(*addtags)
                        messages.add_message(request, messages.SUCCESS, "'{}' {}".format(file.short_name,_('has been tagged')))
                    except:
                        messages.add_message(request, messages.ERROR, "{} '{}'".format(_('an error has occured while tagging'),file.short_name))
                else:
                    messages.add_message(request, messages.WARNING, "{} '{}'".format(_('you do not have permissions to tag'),file.short_name))

        else:
            messages.add_message(request, messages.WARNING, "{}.".format(_('Nothing has been tagged. Tag list is empty.')))

        return redirect(next, folderid=folderid,uid=uid)


class FileRemoveTagsView(View):

    def post(self,request,folderid, uid, next):
        #import ipdb; ipdb.set_trace()

        fileList=request.POST.get("fileList",'')
        if fileList!='':
            fileList= [s for s in fileList.split(",")]

        files=File.objects.filter(uid__in=fileList)
        if len(files)>0:
            for file in files:
                if file.has_perm(request.user.holder,'can_edit'):
                    try:
                        file.subjects.clear()
                        messages.add_message(request, messages.SUCCESS, "'{}' {}".format(file.short_name,_(' tags have been removed')))
                    except:
                        messages.add_message(request, messages.ERROR, "{} '{}'".format(_('an error has occured while untagging'),file.short_name))
                else:
                    messages.add_message(request, messages.WARNING, "{} '{}'".format(_('you do not have permissions to remove tags'),file.short_name))

        else:
            messages.add_message(request, messages.WARNING, "{}.".format(_('Nothing has been untagged. Tag list is empty.')))

        return redirect(next, folderid=folderid, uid=uid)



class FileCopyView(View):

    def post(self,request,folderid,uid,next):

        fileList=request.POST.get("fileList",'')
        if fileList!='':
            fileList= [s for s in fileList.split(",")]
        #import ipdb; ipdb.set_trace()
        files=File.objects.filter(uid__in=fileList)
        folder=get_object_or_404(Folder,id=folderid,uid=uid)
        for file in files:
            if file.has_perm(request.user.holder,'can_read') or file.is_public:
                if folder.has_perm(request.user.holder,'can_add'):
                    folders=[folder,request.user.myfiles]
                else:
                    folders=[request.user.myfiles]
                try:
                    newfile=File.objects.copy(file)
                    newfile.owner=request.user
                    newfile.owner_perms(request.user.holder)
                    newfile.save()
                    newfile.filer_folder_related.add(*folders)
                    messages.add_message(request, messages.SUCCESS, "'{}' {}.".format(file.short_name,_('has been succesfully duplicated')))
                except:
                    messages.add_message(request, messages.ERROR, "{} '{}'".format(_('an error occured while copying'),file.short_name))
            else:
                messages.add_message(request, messages.WARNING, "{} '{}'".format(_('you hav no permissions to copy'),file.short_name))
        return redirect(next, folderid=folderid, uid=uid)

class FileDownloadView(View):

    def post(self,request,folderid,uid,next):
        #import ipdb; ipdb.set_trace()
        from django.core.files.storage import default_storage as DS
        fileList=request.POST.get("fileList",'')
        if fileList!='':
            fileList= [s for s in fileList.split(",")]
        files=File.objects.filter(uid__in=fileList)
        for file in files:
            if DS.exists(file.file.name):
                    url=file.url
                    dlLink='<a href={} download>{}</a>'.format(file.url,file.short_name)
                    messages.add_message(request, messages.INFO, '{} {}'.format(_('clic to download'), dlLink ))
            else:
                messages.add_message(request, messages.ERROR, '{} {}'.format(file.short_name,_('not find on our servers') ))
        return redirect(next, folderid=folderid, uid=uid)
