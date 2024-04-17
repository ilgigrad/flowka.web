from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import datetime
from core.utils import shortdate
from django.contrib import messages

class MessageManager (models.Manager):

    def fetch(self,request):
        storage = messages.get_messages(request)
        for message in storage:
            new=Message()
            new.user=request.user
            new.is_visible=True
            new.level=message.level
            new.extra_tags=message.extra_tags
            new.message=message.message
            storage.used = True #prevent to erase message after reading: set to False
            new.save()

    def count_unread(self, user):
        return self.filter(user=user,is_visible=True,is_read=False).order_by('-received_at').count()

    def lasts(self, user, max=50):
        messages= self.filter(user=user,is_visible=True).order_by('-received_at')[:max]
        return messages

    def unread(self, user):
        messages= self.filter(user=user,is_visible=True,is_read=False).order_by('-received_at')
        return messages

    def read(self,user):
        return self.filter(user=user,is_visible=True,is_read=False).order_by('-received_at').update(is_read=True)

    def read_or_last(self,user, max=20):
        c=self.count_unread(user)
        if c>0:
            return self.unread(user) | self.lasts(user,c+max)[c:max]
        else:
            return self.lasts(user,max)

    def purge(self,user):
        import datetime as dt
        somedays=dt.datetime.now() - dt.timedelta(days=2)
        longago=dt.datetime.now() - dt.timedelta(days=180)
        purge=self.filter(is_read=True,received_at__lte=lastweek,user=user).delete()[0]
        purge+=self.filter(received_at__lte=longago,user=user).delete()[0]
        return purge


class Message(models.Model):
    # MESSAGE_TAGS = {
    #     00: 'TINY',
    #     05: 'DEBUG',
    #     10: 'PROCESS',
    #     15: 'LIAISON',
    #     30: 'INFO',
    #     40: 'SUCCESS',
    #     50: 'WARNING',
    #     60: 'ERROR',
    #     70: 'CRITICAL'
    # }
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='send_to_%(app_label)s_%(class)s', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('user'))
    received_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)
    is_visible = models.BooleanField(_('is visible'), default=True)
    is_read = models.BooleanField(_('is read'), default=False)
    level = models.IntegerField(_('status'), default=0)
    extra_tags = models.CharField(max_length=50,default='', blank=True, null=True, verbose_name=_('extra tag'))
    message = models.CharField(max_length=255,default='', blank=True, null=True, verbose_name=_('message'))

    @property
    def tags(self):
        return settings.MESSAGE_TAGS[self.level].lower()

    @property
    def is_unread(self):
        if self.is_read:
            return False
        else:
            self.is_read=True
            self.save()
            return True


    objects=MessageManager()
