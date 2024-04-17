from django.db.models import CharField
from core.custom_validators import validate_color
from django.utils.translation import ugettext_lazy as _


class ColorField(CharField):
    description = "validate color string format"

    def __init__(self, *args, default, verbose_name, **kwargs):
        kwargs['max_length'] = 7
        kwargs['default'] = default
        kwargs['verbose_name']=verbose_name
        kwargs['validators'] = [validate_color]
        super(ColorField, self).__init__(*args, **kwargs)

    
