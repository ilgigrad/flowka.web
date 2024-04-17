from enum import Enum
from django.db import models
from django.contrib.auth.models import  AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_countries.fields import CountryField
from filer.mixins import AvatarMixin
from tagulous.models import TagField
from tag.models import TagSubject
from account.perms import PermMixin,PermHolderMixin
from core.mixins import EnumMixin
from core.utils import listIfNot
from django.utils.functional import cached_property
from uuid import uuid1

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser,PermHolderMixin):
    """User model."""
    uid = models.CharField(max_length=36, null=True, blank=True, unique=True)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), unique=False, max_length=100)
    last_name = models.CharField(_('last name'), unique=False, max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @cached_property
    def myfiles(self):
        from filer.models import Folder
        return Folder.objects.myfiles(self)

    @cached_property
    def myfavs(self):
        from filer.models import Folder
        return Folder.objects.myfavs(self)

    @property
    def myfolders(self):
        from filer.models import Folder
        return self.get_all_with_label(Folder,'can_add')

    @property
    def m_unread(self):
        from message.models import Message
        return Message.objects.count_unread(self)

    def __init__(self, *args, **kwargs):
        super(User,self).__init__(*args,**kwargs)
        if self.uid is None or self.uid=='':
            self.uid=str(uuid1())

class UserProfile(AvatarMixin): #if mixin inherits from models.model, then class can't inherit from models.Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,null=True)
    organization = models.CharField(_('organization'), null=True,unique=False, max_length=100)
    website = models.URLField(blank=True, null=True)
    city = models.CharField(_('city'), unique=False, max_length=100, null=True)
    country = CountryField(blank_label=_('select country'), null=True)
    subscribe_newsletter = models.BooleanField(default=False)
    language = models.CharField(max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE)
    interests = TagField(TagSubject)

    User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

    def save(self, *args,**kwargs):
        #import ipdb; ipdb.set_trace()
        self.city=(self.city or '').lower()
        self.organization=(self.organization or '').lower()
        super(UserProfile, self).save(*args,**kwargs)
        #self.user.save()

    def set_first_name(self,first_name):
        self.user.first_name=first_name

    def get_first_name(self):
        return self.user.first_name

    first_name = property(get_first_name,set_first_name)

    def set_last_name(self,last_name):
        self.user.last_name=last_name

    def get_last_name(self):
        return self.user.last_name

    last_name = property(get_last_name,set_last_name)

    def set_email(self,email):
        self.user.email=email

    def get_email(self):
        return self.user.email

    email = property(get_email,set_email)

    @property
    def get_full_name(self):
        if not self.first_name:
            return
        return ' '.join([self.first_name, self.last_name])

    @property
    def get_login_name(self):
        if self.first_name:
            return self.first_name
        return self.email



####  GROUP EXTEND ######

class TeamManager(models.Manager):
    def personal_team(self,user):
        users=listIfNot(user)
        teams=self.filter(
            user__in=users,
            _access=Team.TEAM_ACCESS.get_value('personal')
        )
        return teams


class Team(PermMixin,PermHolderMixin,models.Model):
    class TEAM_ACCESS(EnumMixin,Enum):
        noaccess    = (0,'noaccess')
        personal = (1,'personal')
        hidden   = (2,'hidden')
        private  = (3,'private')
        public   = (4,'public')

    class TEAM_NAMES(EnumMixin,Enum):
        connected    = ('connected','connected persons')
        blocked  = ('blocked', 'blocked persons')
        suggested = ('suggested', 'suggested persons')

    uid = models.CharField(max_length=36, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100,null=False,default='')
    user  = models.ManyToManyField(getattr(settings, 'AUTH_USER_MODEL'))
    _access = models.IntegerField(_('access'), default=TEAM_ACCESS.get_value('noaccess'),choices=[x.value for x in TEAM_ACCESS])

    objects=TeamManager()

    def __str__(self):
        return "id:%s | %s" % (
            str(self.id),
            self.name,
        )

    def __init__(self, *args, **kwargs):
        super(Team,self).__init__(*args,**kwargs)
        if self.uid is None or self.uid=='':
            self.uid=str(uuid1())

    def get_access(self):
        return self.get___access_display()

    def set_access(self,access='noaccess'):
        try:
            self._access=self.TEAM_ACCESS.get_value(access)
        except:
            pass

    access = property(get_access,set_access)

    @property
    def is_personal(self):
        return self._access == self.TEAM_ACCESS.get_value('personal')




class TeamProfile(AvatarMixin):  #if mixin inherits from models.model, then class can't inherit from models.Model
        team = models.OneToOneField(Team, on_delete=models.CASCADE)
        description=models.TextField(null=True, blank=True, verbose_name=_('description'))
        website = models.URLField(blank=True, null=True)


import account.signals
