
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from .models import Column
from .forms import ColumnForm,TimeColumnForm,SplitColumnForm,RegexColumnForm,SubstrColumnForm
from message.models import Message
from django.contrib import messages



# Create your views here.
class ColumnView(View):

    def get(self,request,uid,columnid):
        column = get_object_or_404(Column.objects.select_related('dataset'), id=columnid, dataset__datafile__uid=uid)
        if column.dataset.datafile.has_perm(request.user.holder,'can_edit'):
            context={
                'columnform':ColumnForm(instance=column),
                'rename':column.rename,
                'columnid':columnid,
                'uid':uid,
                'restColumnURL':'/datacollect/rest_column/',
                }

            return TemplateResponse(request,'datacollect/column.html', context)
        else:
            messages.add_message(request, messages.ERROR, _('you don\'t have permissions to edit this datafile'))
            Message.objects.fetch(request)


class TimeColumnView(View):

    def get(self,request,uid,columnid):
        column = get_object_or_404(Column.objects.select_related('dataset'), id=columnid, dataset__datafile__uid=uid)
        if column.dataset.datafile.has_perm(request.user.holder,'can_edit'):
            context={
                'subform':TimeColumnForm(instance=column),
                'subkey':'timize',
                'refer':'alter_rule',
                'columnid':columnid,
                'uid':uid,
                }
            #import ipdb; ipdb.set_trace()
            return TemplateResponse(request,'datacollect/subcolumn.html', context)
        else:
            messages.add_message(request, messages.ERROR, _('you don\'t have permissions to edit this datafile'))
            Message.objects.fetch(request)

class SplitColumnView(View):

    def get(self,request,uid,columnid):
        column = get_object_or_404(Column.objects.select_related('dataset'), id=columnid, dataset__datafile__uid=uid)
        if column.dataset.datafile.has_perm(request.user.holder,'can_edit'):
            context={
                'subform':SplitColumnForm(instance=column),
                'subkey':'splitize',
                'refer':'alter_rule',
                'columnid':columnid,
                'uid':uid,
                }
            #import ipdb; ipdb.set_trace()
            return TemplateResponse(request,'datacollect/subcolumn.html', context)
        else:
            messages.add_message(request, messages.ERROR, _('you don\'t have permissions to edit this datafile'))
            Message.objects.fetch(request)

class SubstrColumnView(View):

    def get(self,request,uid,columnid):
        column = get_object_or_404(Column.objects.select_related('dataset'), id=columnid, dataset__datafile__uid=uid)
        if column.dataset.datafile.has_perm(request.user.holder,'can_edit'):
            context={
                'subform':SubstrColumnForm(instance=column),
                'subkey':'ssubstrize',
                'refer':'alter_rule',
                'columnid':columnid,
                'uid':uid,
                }
            #import ipdb; ipdb.set_trace()
            return TemplateResponse(request,'datacollect/subcolumn.html', context)
        else:
            messages.add_message(request, messages.ERROR, _('you don\'t have permissions to edit this datafile'))
            Message.objects.fetch(request)

class RegexColumnView(View):

    def get(self,request,uid,columnid):
        column = get_object_or_404(Column.objects.select_related('dataset'), id=columnid, dataset__datafile__uid=uid)
        if column.dataset.datafile.has_perm(request.user.holder,'can_edit'):
            context={
                'subform':RegexColumnForm(instance=column),
                'subkey':'regexize',
                'refer':'alter_rule',
                'columnid':columnid,
                'uid':uid,
                }
            #import ipdb; ipdb.set_trace()
            return TemplateResponse(request,'datacollect/subcolumn.html', context)
        else:
            messages.add_message(request, messages.ERROR, _('you don\'t have permissions to edit this datafile'))
            Message.objects.fetch(request)
