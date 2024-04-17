from django.shortcuts import  get_object_or_404, redirect
from filer.models import Folder
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from core.utils import get_session
from filer.forms import FolderForm
from django.views.generic import View

class SortView():

    def get(self,request):

        context=get_session(request,'context')
        #user clic on paginator or sort button =>filters remain the same
        context['previous']=context.get('order','')
        context['order']=request.GET.get('order','')
        if context['order']!='' and context['order']==context['previous'] :
            context['direction'] = not context.get('direction',False)
        else:
            context['direction'] =False

        request.session['context']=context
        return


class FolderView():

    def get(self,request,folderid,uid):
        context=get_session(request,'context')

        if folderid==0 or folderid=='0':
            try:
                id=context['folders']['current']['id']
                uid=context['folders']['current']['uid']
            except:
                id=Folder.objects.filter(is_root=True,is_public=True).first().id
                uid=Folder.objects.filter(is_root=True,is_public=True).first().uid
        else:
            id=folderid
            uid=uid
        context['folders']=Folder.objects.get_folders_from_id(id,uid,request.user)
        request.session['context']=context
        return id,uid

class FolderCreateView(View):

    def get(self,request):
        return FolderForm(initial={'name':_('new folder'),'description':''})

    def post(self,request,folderid,uid,next):
        context=get_session(request,'context')
        form=FolderForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data.get('name','new_folder')
            description=form.cleaned_data.get('description','')
            newFolder=form.save()
            newFolder.is_public=False
            newFolder.is_root=False
            newFolder.parent=get_object_or_404(Folder,id=folderid,uid=uid)
            newFolder.owner=request.user
            newFolder.owner_perms(request.user.holder)
            newFolder.save()
            context['folders']=Folder.objects.get_folders_from_id(folderid,uid,request.user)
            request.session['context']=context
            messages.add_message(request, messages.SUCCESS, "{} {}".format(newFolder.name,_('has been created')))
        return redirect(next, folderid=newFolder.id, uid=newFolder.uid)

class FolderUpdateView(View):

    def get(self,request,folderid,uid):
        folder=get_object_or_404(Folder,id=folderid, uid=uid)
        return FolderForm(initial={'name':folder.name,'description':folder.description})

    def post(self,request,folderid,uid,next):
        context=get_session(request,'context')
        form=FolderForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data.get('name','new_folder')
            description=form.cleaned_data.get('description','')
            folder=get_object_or_404(Folder,id=folderid,uid=uid)
            if folder.has_perm(request.user.holder,'can_edit'):
                folder.name=name
                folder.description=description
                folder.save()
                messages.add_message(request, messages.INFO, "{} {} {}".format(_('folder'),folder.name,_('has been updated')))
                context['folders']['current']['id']=folder.id
                context['folders']['current']['uid']=folder.uid
                context['folders']['current']['name']=folder.name
                context['folders']['current']['description']=folder.description
            else:
                messages.add_message(request, messages.WARNING, "{} {}".format(_('you do not have enough privilege to update folder'),folder.name))
        request.session['context']=context
        return redirect(next, folderid=folder.id, uid=folder.uid)

class FolderDeleteView(View):

    def get(self,request,folderid,uid, next):
        #import ipdb; ipdb.set_trace()
        folder=get_object_or_404(Folder,id=folderid,uid=uid)
        if folder.has_perm(request.user.holder,'can_delete'):
            try:
                folder.delete()
                messages.add_message(request, messages.INFO, "{} {}".format(folder.name,_('has been deleted')))
            except:
                messages.add_message(request, messages.DEBUG, "{} {}".format(folder.name,_('has not been deleted, something weard has happened')))
        context=get_session(request,'context')
        context['folders']=Folder.objects.get_folders_from_id(folder.parent.id,folder.parent.uid,request.user)
        request.session['context']=context
        return redirect(next, folderid=folder.parent.id,uid=folder.parent.uid)
