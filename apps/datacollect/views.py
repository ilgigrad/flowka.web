
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from datacollect.models import DataSet
#from .columns.forms import ColumnForm
from filer.models import File
from filer.forms import  FileShortForm, FileSubjectsForm
from message.models import Message
from django.contrib import messages
from core.utils import get_form_errors_list



# Create your views here.
class SnippetEditView(View):

    def getContext(self,datafile,dataset,next):
        #dataset.templatize()
        return {
            'clean':("disabled","enabled")[dataset.clean_cols is None],
            'values':dataset.origin_rows,
            'heads':dataset.origin_cols,
            'maxWidth':dataset.max_snippet_width,
            'prec':next,
            'next':"datacollect:snippet",
            'file':datafile,
            'subjects_form':FileSubjectsForm(instance=datafile),
            #'column_form':ColumnForm(),
            #'cols':dataset.origin_cols[1:], #the transform information
            'column':'col', #wether the column title appears in row or in col in the spreadsheets
            'counts':dataset.counts,
            'columnURL':'/datacollect/column/',
            }

    def get(self,request,uid,next):
        dataset = get_object_or_404(DataSet, datafile__uid=uid)
        datafile = get_object_or_404(File, uid=uid)
        context=self.getContext(datafile,dataset,next)

        return TemplateResponse(request,'datacollect/dc_edit.html', context)

    def post(self,request,uid,next):
        #import ipdb; ipdb.set_trace()
        datafile = get_object_or_404(File, uid=uid)
        dataset = get_object_or_404(DataSet, datafile__uid=uid)
        if datafile.has_perm(request.user.holder,'can_edit'):
            file_form = FileShortForm(data=request.POST or None, instance=datafile)
            subjects_form=FileSubjectsForm(data=request.POST or None , instance=datafile)
            if file_form.is_valid() and subjects_form.is_valid():
                if file_form.has_changed():
                    file_form.save()
                if  subjects_form.has_changed():
                    subjects_form.save()
            else:
                for error in get_form_errors_list(file_form.errors)+get_form_errors_list(subjects_form.errors):
                    messages.add_message(request, messages.ERROR, error)
            dataset.save()
        else:
            messages.add_message(request, messages.ERROR, _('you don\'t have permissions to edit this datafile'))
        Message.objects.fetch(request)
        context=self.getContext(datafile,dataset,next)
        return TemplateResponse(request,'datacollect/dc_edit.html', context)


class MetaEditView(View):

    def getContext(self,datafile, dataset,next):
        dataset.templatize()
        return {
            'clean':("disabled","enabled")[dataset.clean_cols is None],
            'values':dataset.meta_rows,
            'heads':dataset.meta_cols,
            'maxWidth':dataset.max_meta_width,
            'prec':next,
            'next':"datacollect:meta",
            'file':datafile,
            'subjects_form':FileSubjectsForm(instance=datafile),
            #'column_form':ColumnForm(),
            'cols':dataset.origin_cols[1:], #the transform information
            'column':'row', #wether the column title appears in row or in col in the spreadsheets
            'counts':dataset.counts,
            'columnURL':'/datacollect/column/',
            }

    def get(self,request,uid,next):
        dataset = get_object_or_404(DataSet, datafile__uid=uid)
        datafile = get_object_or_404(File, uid=uid)
        context=self.getContext(datafile,dataset,next)
        #import ipdb; ipdb.set_trace()
        return TemplateResponse(request,'datacollect/dc_edit.html', context)

    def post(self,request,uid,next):
        datafile = get_object_or_404(File, uid=uid)
        if datafile.has_perm(request.user.holder,'can_edit'):
            file_form = FileShortForm(data=request.POST or None, instance=datafile)
            subjects_form=FileSubjectsForm(data=request.POST or None , instance=datafile)
            if file_form.is_valid() and subjects_form.is_valid():
                if file_form.has_changed():
                    file_form.save()
                if  subjects_form.has_changed():
                    subjects_form.save()
            else:
                for error in get_form_errors_list(file_form.errors)+get_form_errors_list(subjects_form.errors):
                    messages.add_message(request, messages.ERROR, error)
                Message.objects.fetch(request)
        else:
            messages.add_message(request, messages.ERROR, _('you don\'t have permissions to edit this datafile'))
        dataset = get_object_or_404(DataSet, datafile__uid=uid)
        context=self.getContext(datafile,dataset,next)
        return TemplateResponse(request,'datacollect/dc_edit.html', context)

class DataCleanView(View):

    def getContext(self,datafile,dataset,next):
        dataset.templatize()
        return {
            'clean':("disabled","enabled")[dataset.clean_cols is None],
            'values':dataset.clean_rows,
            'heads':dataset.clean_cols,
            'maxWidth':dataset.max_clean_width,
            'prec':next,
            'next':"datacollect:data",
            'file':datafile,
            'subjects_form':FileSubjectsForm(instance=datafile),
            #'column_form':ColumnForm(),
            'cols':dataset.origin_cols[1:], #the transform information
            'column':'col', #wether the column title appears in row or in col in the spreadsheets
            'counts':dataset.counts,
            'columnURL':'/datacollect/column/',
            }

    def get(self,request,uid,next):
        dataset = get_object_or_404(DataSet, datafile__uid=uid)
        datafile = get_object_or_404(File, uid=uid)
        context=self.getContext(datafile,dataset,next)
        return TemplateResponse(request,'datacollect/dc_edit.html', context)


    def post(self,request,fileid,uid,next):
        datafile = get_object_or_404(File, uid=uid)
        if datafile.has_perm(request.user.holder,'can_edit'):
            file_form = FileShortForm(data=request.POST or None, instance=datafile)
            subjects_form=FileSubjectsForm(data=request.POST or None , instance=datafile)
            if file_form.is_valid() and subjects_form.is_valid():
                if file_form.has_changed():
                    file_form.save()
                if  subjects_form.has_changed():
                    subjects_form.save()
            else:
                for error in get_form_errors_list(file_form.errors)+get_form_errors_list(subjects_form.errors):
                    messages.add_message(request, messages.ERROR, error)
                Message.objects.fetch(request)
        else:
            messages.add_message(request, messages.ERROR, _('you don\'t have permissions to edit this datafile'))
        dataset = get_object_or_404(DataSet, datafile__uid=uid)
        context=self.getContext(datafile,dataset,next)
        return TemplateResponse(request,'datacollect/dc_edit.html', context)
