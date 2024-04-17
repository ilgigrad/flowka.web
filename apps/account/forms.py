from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from core.custom_forms_fields import ExtEmailField, NameField, PhoneField
from core.forms import MultipleForm
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from account.models import UserProfile
from django.contrib.auth.models import User
from filer.forms import CropForm
from tagulous.forms import TagField
from core.mixins import NextFormMixin

class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=200, widget=forms.EmailInput(attrs={'autocomplete':_('email')}),help_text=_('Required'))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'autocomplete':_('new password')}))

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')
    email = ExtEmailField(max_length=200, help_text=_('Required'), widget=forms.EmailInput(attrs={'autocomplete':_('email')}))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'autocomplete':_('password')}))
    password2 = forms.CharField(label=_("confirm Password"), widget=forms.PasswordInput(attrs={'autocomplete':_('confirm password')}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone', 'website','city','country','organization','subscribe_newsletter')

    def __init__(self, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        user = kwargs.pop('user',None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if not self.instance.user:
            self.instance.user=user
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    last_name = NameField(
        label=_('last name'),
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': _('last name'), 'id':'lastname'}),
        required=True,
        )

    first_name = NameField(
        label='first name',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': _('first name'), 'id':'firstname'}),
        required=True,
        )

    phone = PhoneField(
        label='telephone',
        widget=forms.TextInput(attrs={'placeholder': _('telephone'), 'id':'phone'}),
        required=False,
        )

    website = forms.URLField(
        required=False,
        max_length=50,
        initial='http://'
        )

     # photo = forms.ImageField(
     #     required=False,
     #     widget=forms.FileInput
     #     )

    subscribe_newsletter = forms.BooleanField(
        required=False,
        label_suffix='',
        widget=forms.CheckboxInput(attrs={'id':'subscribe_newsletter'})
        )

    city = NameField(
        label=_('city'),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('city'), 'id':'city'}),
        )

    country = CountryField().formfield()

    organization = forms.CharField(
        label=_('organization'),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('organization'), 'id':'organization'}),
        )

#    def __init__(self, *args, **kwargs):
#        super(ProfileForm, self).__init__(*args, **kwargs)
#        self.fields['action'].initial = 'profile'

    def save(self,*args, **kwargs):
        profile=super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name').lower()
        self.instance.user.last_name = self.cleaned_data.get('last_name').lower()
        self.instance.user.save()
        return profile

class UserInterestsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('interests',)

    interests=TagField(
        label=_('interests'),
        required=False,)
