from django.shortcuts import redirect
from django.template.response import TemplateResponse
from survey.models import Survey2019
from survey.forms import  Survey2019Form
from django.views.generic import View
from core.utils import get_session,get_form_errors_list, get_client_ip
from django.contrib import messages
from message.models import Message
from django.utils.translation import ugettext as _
from datetime import datetime
# Create your views here.

class SurveyView(View):

    def get(self,request):
        #import ipdb; ipdb.set_trace()
        try:
            lastSurvey=Survey2019.objects.get(ip=get_client_ip(request),browser=request.META.get('HTTP_USER_AGENT',''))
            return TemplateResponse(request,'survey/redo2019.html', {'next':'survey:survey2019'})
        except:
            return TemplateResponse(request,'survey/intro2019.html', {'next':'survey:survey2019'})


class Survey2019View(View):

    def get(self,request):
        #import ipdb; ipdb.set_trace()
        try:
            lastSurvey=Survey2019.objects.get(ip=get_client_ip(request),browser=request.META.get('HTTP_USER_AGENT',''))
            form=Survey2019Form(instance=lastSurvey)
        except:
            form=Survey2019Form()
        return TemplateResponse(request,'survey/survey2019.html', {'next':'survey:survey2019', 'fillform':form})


    def post(self,request):
        #import ipdb; ipdb.set_trace()
        try:
            lastSurvey=Survey2019.objects.get(ip=get_client_ip(request),browser=request.META.get('HTTP_USER_AGENT',''))
            form=Survey2019Form(request.POST,instance=lastSurvey)
        except:
            form=Survey2019Form(request.POST)

        if form.is_valid():
            #import ipdb; ipdb.set_trace()
            survey2019=form.save()
            survey2019.ip=get_client_ip(request)
            survey2019.browser=request.META.get('HTTP_USER_AGENT','')
            survey2019.save()
            return redirect ('home:home')
                #redirect ('survey:survey2019', {'page': page+1})
        return TemplateResponse(request,'survey/survey2019.html', {'next':'survey:survey2019','fillform':form})
