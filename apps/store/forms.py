from django.forms import Form, TextInput, EmailInput, CharField, Textarea
from core.custom_forms_fields import ExtEmailField, NameField, PhoneField
from django.utils.translation import ugettext as _
from django.utils.text import format_lazy

class SubscriptForm(Form):

    email = ExtEmailField(
        label='email',
        widget=EmailInput(attrs={'placeholder': _('email'), 'id':'email'}),
        required=True
        )
    phone = PhoneField(
        label='telephone',
        widget=TextInput(attrs={'placeholder': _('telephone'), 'id':'phone'}),
        required=False
        )
    firstname = NameField(
        label='first name',
        max_length=50,
        widget=TextInput(attrs={'placeholder': _('first name'), 'id':'firstname'}),
        required=True
        )
    lastname = NameField(
        label='last name',
        max_length=50,
        widget=TextInput(attrs={'placeholder': _('last name'), 'id':'lastnameame'}),
        required=True
        )


class ContactForm(Form):

    remain=_('remain')
    exceed=_('exceed')

    email = ExtEmailField(
        label='email',
        widget=EmailInput(attrs={'placeholder': _('email'), 'id':'email'}),
        required=True
        )
    subject = CharField(
        label='subject',
        max_length=100,
        widget=TextInput(attrs={'placeholder': _('subject of the message'), 'id':'subject'}),
        required=True
        )
    message = CharField(
        label='message',
        max_length=1000,
        widget=Textarea(attrs={'placeholder': _('type your message'), 'id':'id_contact_message','onkeyup':"textCount(this);"}),
        required=True
        )
