from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.translation import get_language,  check_for_language, activate as lang_activate, LANGUAGE_SESSION_KEY
from django.utils.translation import ugettext as _
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.


@login_required

def private(request):
    context={'message':'You can access this private page'}
    context['title']='Private Page'
    return TemplateResponse(request,'message/message.html', context)

def privacy(request):
    context={'title':_(' Privacy Policy')}
    return TemplateResponse(request,'home/privacy.html', context)

def legal(request):
    context={'title':_('Terms of Service')}
    return TemplateResponse(request,'home/legal.html', context)

def overview(request):
    context={'title':_('Overview')}
    return TemplateResponse(request,'home/overview.html', context)


def hello(request):
    if request.user.is_authenticated:
        context={'message':"Salut, {0} !".format(request.user.profile.get_login_name)}
    else:
        context={'message':"Salut, anonyme."}
    context['title']='Say hello'
    return TemplateResponse(request,'message/message.html', context)

def home(request):
    context={'homebg':True}
    return TemplateResponse(request,'home/home.html',context)

def support(request):
    context={'homebg':True}
    return TemplateResponse(request,'home/support.html',context)

def slider(request):
    return TemplateResponse(request,'home/slider.html')



class ParametersView(View):

    def __init__(self,*args,**kwargs):
        self.context={}
        self.context['homebg']=True
        super().__init__()

    def get(self,request):
        return TemplateResponse(request,'home/parameters.html',self.context)

    def post(self,request):
        # set the response as it will be used for updating session
        #import ipdb; ipdb.set_trace()
        # set the language
        lang_code=request.POST.get('language')
        if lang_code and check_for_language(lang_code):
            response=TemplateResponse(request,'info.html')
            if hasattr(request, 'session'):

                request.session[LANGUAGE_SESSION_KEY] = lang_code
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
                                    max_age=settings.LANGUAGE_COOKIE_AGE,
                                    path=settings.LANGUAGE_COOKIE_PATH,
                                    domain=settings.LANGUAGE_COOKIE_DOMAIN)
            lang_activate(lang_code)
            if request.user.is_authenticated:
                    request.user.profile.language=lang_code
                    request.user.profile.save()
        else:
            self.context['errors']=[_("something wrong has happened")]
            return TemplateResponse(request,'home/parameters.html', self.context)
        next = request.POST.get('next',None)
        if next:
            return redirect(next)
        self.context['info']={'desc':'your parameters have been successfully updated','title':'PARAMETERS SAVED !'}
        return TemplateResponse(request,'info.html', self.context)

def next(request):
    next = request.POST.get('next', 'home/home.html')
    return HttpResponseRedirect(next)


def error_page(request,errid):
    return TemplateResponse(request,errid+'.html')
