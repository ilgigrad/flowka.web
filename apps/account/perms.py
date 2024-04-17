from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from core.utils import listIfNot
from uuid import uuid4

class Holder(models.Model):
    uiid = models.CharField(max_length=8, default=uuid4().hex[:8], editable=False)
    is_user = models.BooleanField(_('is a user'), default=True, blank=False)
    pass

class PermManager (models.Manager):
    """
        return the perm object for an object instance and a codename
    """
    PERMS={
        'add':'can_add', #add a member to a team or a file to a folder
        'remove':'can_remove', # remove a member from a team or a file from a folder
        'delete':'can_delete',# can suppress a user or a file or a folder
        'read':'can_read', # can read a file or the content/user of a team
        'write':'can_write', #can modify a file
        'edit':'can_edit', #can edit informations as label or descriptions
        'share':'can_share', #can share a file or a folder
        'copy':'can_copy', #can share a file or a folder
        'list':'can_list', #list folders or teams
        'grant':'can_grant', #can grant perms
    }
    OWNER_PERMS=[
        PERMS['read'],PERMS['write'],PERMS['list'],PERMS['edit'],
        PERMS['add'],PERMS['delete'],PERMS['remove'],PERMS['share'],PERMS['copy']]
    PUBLIC_PERMS=[
        PERMS['read'],PERMS['list'],
        PERMS['share'],PERMS['copy']]
    READER_PERMS=[PERMS['read'],PERMS['list']]
    ACCESS_PERMS=[PERMS['read'],PERMS['add'],PERMS['remove'],PERMS['list']]

    def add_perms(self,holder,label):
        perms=[]
        holders=listIfNot(holder)
        labels=listIfNot(label)
        for holder in holders:
            for label in labels:
                perm,created=self.get_or_create(holder=holder,perm_label=label)
                perms+=[perm]
        return perms

    def access_perms(self,holder):
        return self.add_perms(holder,self.ACCESS_PERMS)

    def owner_perms(self,holder):
        return self.add_perms(holder,self.OWNER_PERMS)

    def public_perms(self,holder):
        return self.add_perms(holder,self.PUBLIC_PERMS)

    def reader_perms(self,holder):
        return self.add_perms(holder,self.READER_PERMS)


class Perm(models.Model):
    """
    extend permissions to instance of objects
    """
    holder = models.ForeignKey(
        Holder,
        models.CASCADE,
        verbose_name=_('holder'),
        null=True
    )
    perm_label = models.CharField(_('permission label'), max_length=20,default='')
    objects = PermManager()

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        unique_together = (('holder', 'perm_label',),)
        ordering = ('holder', 'perm_label',)
        #            'objid','codename',)

    def __str__(self):
        return "id:%s | %s" % (
            str(self.id),
            self.perm_label,
        )
    def __init__(self,*args,**kwargs):
        super(Perm,self).__init__(*args,**kwargs)
        self.holder = kwargs.pop('holder',None)
        self.perm_label  = kwargs.pop('perm_label',None)
        for i in range(len(args)):
            if self.holder is None and isinstance(args[i],Holder):
                self.holder=args[i]
            elif self.perm_label is None and (isinstance(args[i],str)):
                self.perm_label=args[i]

class PermMixin(models.Model):
    """
        set permissions methods and attributes for the class to grant permissions to
    """
    perms = models.ManyToManyField(
        Perm,
        verbose_name=_('object permissions'),
        blank=True,
        help_text=_('Specific permissions by object.'),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    class Meta:
        abstract = True
        #unique_together = (('content_type', 'objid','codename',),)

    def get_perms_labels(self,holder):
        """
            get permissions labels that has a holder on a instance of a class
        """
        return self.perms.filter(holder=holder).values_list('perm_label', flat=True)

    def has_perm(self,holder,label):
        """
            return wether or not a holder has a perm on a instance of a class
        """
        return self.perms.filter(holder=holder,perm_label=label).last() is not None

    def get_perms(self,holder):
        """
            return the perm object associate to a holder for a perm value
        """
        return self.perms.filter(holder=holder)

    def add_perms(self,holder,labels):
        """
            add perms to an object for a user of a list of users
        """
        perms=Perm.objects.add_perms(holder,labels)
        self.perms.set(perms)
        self.save()
        return perms

    def access_perms(self,holder):
        """ give holder perms to the user(s) for the instance object
        """
        perms=Perm.objects.access_perms(holder) #create perms if don't exist
        self.remove_perms(holder,None)   #remove previous
        self.perms.set(perms) #attach perms to the object
        return perms

    def owner_perms(self,holder):
        """ give holder perms to the user(s) for the instance object
        """
        perms=Perm.objects.owner_perms(holder) #create perms if don't exist
        self.remove_perms(holder,None)   #remove previous
        self.perms.set(perms) #attach perms to the object
        return perms

    def public_perms(self,holder):
        """ give public perms to the user(s) for the instance object
        """
        perms=Perm.objects.public_perms(holder)#create perms if don't exist
        self.remove_perms(holder,None)  #remove previous
        self.perms.set(perms) #attach perms to the object
        return perms


    def reader_perms(self,holder):
        """ give reader perms to the user(s) for the instance object
        """
        perms=Perm.objects.reader_perms(holder)#create perms if don't exist
        self.remove_perms(holder,None)  #remove previous
        self.perms.set(perms) #attach perms to the object
        return perms

    def remove_perms(self,holder=None,label=None):
        """
            remove set of permissions attached to an object of the instance
        """
        #import ipdb; ipdb.set_trace()
        if holder is None and label is None:
            self.perms.clear()
        elif holder is None and label is not None:
            labels=listIfNot(label)
            self.perms.remove(*self.perms.filter(perm_label__in=labels))
        elif holder is not None and label is not None:
            labels=listIfNot(label)
            holders=listIfNot(holder)
            self.perms.remove(*self.perms.filter(holder__in=holders,perm_label__in=labels))

    def clean_perms(self):
        """
            remove all permissions attached to the instance of the class
        """
        self.perms.clear()

    @property
    def is_shared(self):
        if self.is_public:
            return True
        elif self.perms.exclude(holder=self.owner.holder).count() >1:
            return True
        return False



class PermHolderMixin(models.Model):
    holder = models.OneToOneField(Holder, on_delete=models.SET_NULL,null=True)

    class Meta:
        abstract = True

    def get_perm(self,obj,label):
        """
            get the permisson of an object for the intance holder
        """
        return obj.perms.filter(holder=self.holder, perm_label=label)

    def get_perms(self,obj):
        """
            get the permissons of an object for the intance holder
        """
        objs=listIfNot(obj)
        perms=[]
        for obj in objs:
            perm+=obj.perms.filter(holder=self.holder).values_list('perms', flat=True)
        return perms

    def get_all_with_label(self,cls,label):
        """
            get all object of a class with a specific permission
        """
        labels=listIfNot(label)
        return cls.objects.filter(perms__holder=self.holder, perms__perm_label__in=labels)


    def has_perm(self,obj,label):
        """
            has the instance holder a specific perm on a object
        """
        if isinstance(self,User) and self.is_superuser and self.is_active:
            return True
        return len(self.get_perms(obj,label))>0

    def add_perms(self,obj,label):
        """
        add perms on an object for a instance holder
        """
        perms=Perm.oject.add_perms(self.holder,label)
        objs=listIfNot(obj)
        for obj in objs:
            obj.perms.set(perms)
        return perms

    def remove_perms(self,obj,label=None):
        """
            remove set of permissions attached to an object of the instance
        """
        if isinstance(obj,list):
            objs=obj
        elif isinstance(obj,type): #obj is a class
            objs=obj.objects.filter(perms__holder=self.holder)
        else:
            objs=[obj]

        for obj in objs:
            if label is None:
                obj.perms.remove(*Perm.objects.filter(holder=self.holder))
            else:
                labels=listIfNot(label)
                obj.perms.remove(*obj.perms.filter(holder=self.holder,perm_label__in=labels))


    def clean_perms(self,cls):
        """
            remove all permissions attached to the holder for the class
        """
        objs=cls.objects.filter(perms__holder=self.holder)
        for obj in objs:
            obj.perms.remove(*Perm.objects.filter(holder=self.holder))

    def access_perms(self,obj):
        perms=Perm.objects.access_perms(self.holder) #create new perms if don't exist
        self.remove_perms(obj)#remove previous perms attached to the object
        objs=listIfNot(obj)
        for obj in objs: #for all objects if many
            obj.perms.set(perms) #attach new perms to the object

    def owner_perms(self,obj):
        perms=Perm.objects.owner_perms(self.holder) #create new perms if don't exist
        self.remove_perms(obj)#remove previous perms attached to the object
        objs=listIfNot(obj)
        for obj in objs: #for all objects if many
            obj.perms.set(perms) #attach new perms to the object


    def reader_perms(self,obj):
        perms=Perm.objects.reader_perms(self.holder) #create new perms if don't exist
        self.remove_perms(obj)#remove previous perms attached to the object
        objs=listIfNot(obj)
        for obj in objs: #for all objects if many
            obj.perms.set(perms) #attach new perms to the object


    def public_perms(self,obj):
        perms=Perm.objects.public_perms(self.holder)  #create new perms if don't exist
        self.remove_perms(obj)#remove previous perms attached to the object
        objs=listIfNot(obj)
        for obj in objs: #for all objects if many
            obj.perms.set(perms) #attach new perms to the object
