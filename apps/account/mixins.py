from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
class OwnerMixin(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='owned_by_%(app_label)s_%(class)s', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('owner'))
    class Meta(): #not really a mixin but an abstract class...
        abstract=True
