from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re


def validate_extemail(value):
    """
    Let's validate the email passed is in a list
    """
    domainext=['com','fr','net','org','eu','gov','us','uk','it','de','dk','be','es','fi','gr','jp','lu','lt','nl','nz','paris','pl','qa','ru','se','tw','at','au','ar','cl','ch','br']
    regex=r"^[a-zA-Z0-9]+([\-\.]?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+([\-]?[a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}$"
    if re.match(regex,value) and not value.split('@')[1].split(".")[1] in domainext:
        raise ValidationError(_("the domain extension of your email address is not allowed yet"), code='invalid_email')


def validate_name(value):
    """
    Let's validate the name field
    """
    regex=r"^[a-zA-Zéèêîûôâàùïöüäëáíóóúñü]+([\-\'\s]?[a-zA-Zéèêîûôâàùïöüäëáíóóúñü]+)*$"
    if not re.match(regex,value):
        raise ValidationError(_("name contains invalid characters"), code='invalid_name')


def validate_phone(value):
    """
    Let's validate the telephone field
    """
    regex=r"^(?:[+]?)(\d?[\-\.\s]?){5,12}$"
    if not re.match(regex,value):
        raise ValidationError(_("Phone number should have a valid format"), code='invalid_phone')


def validate_color(value):
    regex = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    if not re.match(regex,value):
        raise ValidationError(_("Enter a valid color"), 'invalid_color')

def validate_photo_mimetype(value):
    import re
    regex=r'image'
    if not re.match(regex,value.content_type):
        raise ValidationError(_("file is not a valid image"), code='invalid_image')
