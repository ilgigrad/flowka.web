from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Feature(models.Model):
    label = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
       return self.label

    class Meta:
        verbose_name = "Feature"

class Contact(models.Model):
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Prospect"
        verbose_name_plural = "Prospects"
        
    def __str__(self):
       return self.email

class Fee(models.Model):
    reference = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    label = models.CharField(max_length=200)
    picture = models.URLField()
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    features = models.ManyToManyField(Feature, related_name='fees', blank=True)
    subscripted = models.IntegerField(null=False, default=0)


    def __str__(self):
        return self.label

    def strprice(self):
        if self.price is None:
            self.price=0
        return str(self.price).split('.')[0]

    class Meta:
        verbose_name = "Fee"


class Subscription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE) 

    class Meta:
        verbose_name = _("Subscription")

def inc_feesubscripted(sender, instance, **kwargs):

    instance.fee.subscripted+=1
    instance.fee.save()

def dec_feesubscripted(sender, instance, **kwargs):

    instance.fee.subscripted-=1
    instance.fee.save()

pre_save.connect(inc_feesubscripted, sender=Subscription)
pre_delete.connect(dec_feesubscripted, sender=Subscription)



