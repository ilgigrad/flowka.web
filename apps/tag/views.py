from django.shortcuts import redirect
from django.views.generic import View
from tag.forms import TagSearchForm,TagActionForm,TagForm
import re
from core.utils import get_session
from tag.models import TagSubject as TS

class SearchTagView(View):

    def get(self,request):

        context=get_session(request,'context')
        searchTags=context.get('searchTags',[])

        strict=context.get('strict',False)
        context['searchTags']=searchTags
        context['strict']=strict
        request.session['context']=context

        taglist=[]
        for st in searchTags:
            tag=TS(name=st,label=st)
            taglist.append(tag)

        return TagForm(data={'tags':taglist, 'strict':strict})

    def post(self,request,next):
        #import ipdb; ipdb.set_trace()
        form=TagSearchForm(request.POST)
        if form.is_valid():
            searchTags=form.cleaned_data.get('tags',[])
            strict=form.cleaned_data.get('strict',False)
        context=get_session(request,'context')
        context['searchTags']=searchTags
        context['strict']=strict
        request.session['context']=context
        return redirect(next)


class AddTagView():

    def get(self,request):
        context=get_session(request,'context')
        addTags=context.get('addTags',[])
        context['addTags']=addTags
        request.session['context']=context
        taglist=[]
        for at in addTags:
            tag=TS(name=at,label=at)
            taglist.append(tag)
        return TagForm(data={'tags':taglist}) #saarchTags modified 20190130

    def post(self,request):
        form=TagForm(request.POST)
        context=get_session(request,'context')
        addTags=context.get('addTags',[])
        if form.is_valid():
            addTags=form.cleaned_data.get('tags',addTags)
        context['addTags']=addTags
        request.session['context']=context
        #import ipdb; ipdb.set_trace()
        return addTags
