from django.shortcuts import  redirect, get_object_or_404,render_to_response
from django.contrib.auth import get_user_model, authenticate, login as signin, logout as signout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import format_html
from django.utils.encoding import force_bytes, force_text
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db import transaction, IntegrityError
from django.views.generic import View
from django.utils.translation import ugettext as _
from django.conf import settings
from .tokens import account_activation_token
from .forms import LoginForm,SignupForm,UserProfileForm, UserInterestsForm
from filer.forms import CropForm
from .models import UserProfile
from filer.models import File
from django.utils.translation import check_for_language, activate  as lang_activate, LANGUAGE_SESSION_KEY
from django.conf import settings
from core.utils import get_form_errors_list
from message.models import Message


class LoginView(View):

    def __init__(self,*args,**kwargs):
        self.context={}
        self.context['homebg']=True
        super().__init__()

    def get(self, request):
        form = LoginForm()
        self.context["form"]=form
        return TemplateResponse(request,'account/login.html', self.context)

    def post(self,request):
        form = LoginForm(request.POST)

        if form.is_valid():
            if not request.POST.get('remember_me', False):
                request.session.set_expiry(0)
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                signin(request,user)  # nous connectons l'utilisateur
                #return TemplateResponse(request, 'account/login.html', locals())
                self.context['homebg']=False
                self.context['title']='login'
                self.context['info']={'desc':_('You are now a logged as {0}').format(user.profile.get_login_name)}
                response = TemplateResponse(request,'info.html', self.context)
                lang_code = user.profile.language
                if lang_code and check_for_language(lang_code):
                    if hasattr(request, 'session'):
                        request.session[LANGUAGE_SESSION_KEY] = lang_code
                    response.set_cookie(
                        settings.LANGUAGE_COOKIE_NAME,
                        lang_code,
                        max_age=settings.LANGUAGE_COOKIE_AGE,
                        path=settings.LANGUAGE_COOKIE_PATH,
                        domain=settings.LANGUAGE_COOKIE_DOMAIN,
                        )
                    lang_activate(lang_code)
                return response
                Message.objects.purge(user)
            else:
                self.context["errors"]=True
        self.context["form"]=form
        return TemplateResponse(request,'account/login.html', self.context)


def logout(request):
    signout(request)
    context={}
    context['homebg']=True
    context['title']=_('logout')
    info={'title':_('logout !'),'desc':_('you have been logout'),'url':reverse('account:login'),'txt':_('Click here to login again.')}
    context['info']=info
    return TemplateResponse(request,'info.html', context)

def password_change_done(request):
    context={}
    context['homebg']=False
    context['title']=_('password')
    info={'title':_('password changed !'),'desc':_('your password have been succesfully changed'),'url':reverse('account:login'),'txt':_('Click here to login.')}
    context['info']=info
    return TemplateResponse(request,'info.html', context)


def signup(request):
    context={}
    context['homebg']=True

    if request.method == 'POST':
        #import ipdb; ipdb.set_trace()
        if request.user:
            signout(request)
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = _('Activate your account.')
            message = render_to_string('account/signup_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = signup_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            try:
                email.send()
                context['title']=_('sign up')
                info={'title':_('SIGNUP!'),'desc':_('an email has been sent to <span class="fl-txt-peach">{}</span><br> Please confirm your email address to complete the registration').format(to_email)}
                context['info']=info
            except:
                context={}
                context['homebg']=True
                context['title']=_('Signup failed')
                info={'title':_('Signup failed !'),'desc':_('Sign up is not allowed yet !'),'url':reverse('account:login'),'txt':_('Click here to login.')}
                context['info']=info
            return TemplateResponse(request,'info.html', context)
        else:
            context['errors']=get_form_errors_list(signup_form.errors)
    next=request.GET.get('next')
    context['form']= SignupForm()
    return TemplateResponse(request,'account/signup.html',context )


def activate(request, uidb64, token):
    context={}
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        signin(request, user)
        # return redirect('home')
        info={'title':_('user activation'),'desc':_('Thank you for your email confirmation. You are now a registred user.')}
    else:
        info={'title':_('user activation'),'desc':_('activation link is invalid.')}
    context['info']=info
    context['homebg']=True
    return TemplateResponse(request,'info.html', context)


def password_reset_done(request):
    context={}
    context['homebg']=False
    context['title']=_('password')
    info={'title':_('password reset'),'desc':_("We've emailed you instructions for setting your password. <br>If they haven't arrived in few minutes, check your spam folder.")}
    context['info']=info

    return TemplateResponse(request,'info.html', context)



class ProfileView(LoginRequiredMixin, View):
    """
        display user profile informations and picture
    """
    def __init__(self,*args,**kwargs):
        self.context={}
        self.context['homebg']=False
        super().__init__()


    def get(self,request):

        # three forms: informations(profile), picture(avatar) and tags (interests)
        # forms are prefixed in order to allow test witch form is send by POST request
        interests_form=UserInterestsForm(instance=request.user.profile, prefix='interests')
        profile_form = UserProfileForm(instance=request.user.profile, prefix='profile')
        avatar_form = CropForm()

        self.context['interests_form']=interests_form
        self.context['avatar_form']=avatar_form
        self.context['profile_form']=profile_form
        self.context['avatar_url']=request.user.profile.avatar_url
        return TemplateResponse(request,'account/profile.html', self.context)

    def post(self,request):
        error=False
        self.context['avatar_url']=request.user.profile.avatar_url
        interests_form = UserInterestsForm(data=request.POST, instance=request.user.profile, prefix='interests')
        profile_form = UserProfileForm(data=request.POST, instance=request.user.profile, prefix='profile')
        avatar_form = CropForm(request.POST, request.FILES)
        avatar_id=request.POST.get('avatar_id', None)
        #import ipdb; ipdb.set_trace()
        if request.POST.get('avatar_fileSave','False')=="True":
            #submit new avatar only

            if avatar_form.is_valid():
                try:
                    #if a new avatar was previously choosen, it is deleted
                    #the former saved avatar is still attached to profile
                    avatar=File.objects.get(id=avatar_id)
                    avatar.delete()
                except:
                    pass
                #new avatar is not public and not valid until it is saved with profile informations
                #save new avatar (temporaly)
                avatar=avatar_form.save(commit=False)[0]
                avatar.is_public=False
                avatar.is_valid=False
                avatar.owner=request.user
                avatar.save()
                #pass id to the template in order to keep informations about avatar.
                #the url allows to show the picture
                self.context['avatar_id']=avatar.id
                self.context['avatar_url']=avatar.url
            else:
                if avatar_form.errors.get('files'):
                    for error in get_form_errors_list(form.errors.get('files')):
                        messages.add_message(request, messages.ERROR, error)
                else:
                    messages.add_message(request, messages.ERROR, "{}".format(_("this image has an invalid format")))
                error=True
        else:

            #click on 'save profile' -> save all forms data
            #temporary avatar is saved
            if profile_form.is_valid() and profile_form.has_changed():
                profile_form.save()

            if interests_form.is_valid() and interests_form.has_changed():
                try:
                    interests=interests_form.save(commit=False)
                    clean=interests_form.cleaned_data
                    #import ipdb; ipdb.set_trace()
                    #[value for value in list2 if value not in list1]
                    for old_tag in request.user.profile.interests.tags:
                        if old_tag not in clean['interests']:
                            request.user.profile.interests.remove(old_tag)
                    for new_tag in clean['interests']:
                        if new_tag not in request.user.profile.interests.tags:
                            request.user.profile.interests.add(new_tag)
                except:
                    messages.add_message(request, messages.WARNING, "{}".format(_("too much tags in your profile")))
                    error=True
                #get the new avatar id if one was choosen previously
                try:
                    #save the new choosen avatar if exists
                    avatar=File.objects.get(id=avatar_id)
                    if ( not avatar.is_public or not avatar.is_valid):
                        avatar.is_public=True
                        avatar.is_valid=True
                        avatar.save()
                    #link the avatar to profile
                    request.user.profile.avatar=avatar
                    request.user.profile.save()
                except:
                    pass

                if not error:
                    self.context['info']={'desc':'your profile has been successfully updated','title':'PROFILE SAVED !'}
                    return TemplateResponse(request,'info.html', self.context)
            else:
                self.context['errors']=get_form_errors_list(profile_form.errors)
                messages.add_message(request, messages.INFO, 'your profile is invalid')
                error=True

        self.context['profile_form']=profile_form
        self.context['avatar_form']=avatar_form
        self.context['interests_form']=interests_form
        self.context['form_media']=interests_form.media
        return TemplateResponse(request,'account/profile.html', self.context)
