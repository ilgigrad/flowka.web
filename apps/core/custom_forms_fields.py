from django.core.validators import validate_email
from django.forms import CharField, FileField, ImageField
from core.custom_validators import validate_extemail, validate_name, validate_phone,validate_photo_mimetype
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_image_file_extension as validate_photo, FileExtensionValidator as validate_datafile




class ExtEmailField(CharField):
    description = _("An email field specific extension")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 120
        kwargs['validators'] = [validate_email,validate_extemail]
        super(ExtEmailField, self).__init__(*args, **kwargs)

class PhoneField(CharField):
    description = "An email field specific extension"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        kwargs['validators'] = [validate_phone]
        super(PhoneField, self).__init__(*args, **kwargs)

class NameField(CharField):
    description = "An email field specific extension"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50
        kwargs['validators'] = [validate_name]
        super(NameField, self).__init__(*args, **kwargs)

class DataFileField(FileField):
    description = _("A FileField specific extension for datasets")
    def __init__(self, *args, **kwargs):
        valid_ext = ['txt','csv','xls','xlsx','json','dat','xml','html','htm','log']
        message=_('Unsupported file type.')
        code=None
        kwargs['validators'] = [validate_datafile(valid_ext, message, code)]
        super(DataFileField,self).__init__(*args,**kwargs)


class PhotoFileField(ImageField):
    description = _("A ImageField specific extension for Photos")

    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_photo,validate_photo_mimetype]
        super(PhotoFileField,self).__init__(*args,**kwargs)
