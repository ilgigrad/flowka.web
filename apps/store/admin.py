from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Subscription, Contact, Fee, Feature
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


class AdminURLMixin(object):

    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__,)
        return reverse("admin:store_%s_change" % (
            content_type.model),
            args=(obj.id,))


# Register your models here.



@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    search_fields = ['label', 'feature.label', 'feature.description']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin,AdminURLMixin):
    list_filter = ['created_at', 'contacted']
    fields = ['created_at', 'contact_link', 'fee_link','contacted']
    readonly_fields = ['created_at', 'contact_link', 'fee_link']

    def has_add_permission(self, request):
        return False

    def fee_link(self, subscription):
        path = "admin:store_fee_change"
        url = self.get_admin_url(subscription.fee)
        return mark_safe("<a href='{}'>{}</a>".format(url, subscription.fee.label))

    def contact_link(self, subscription):
        url = self.get_admin_url(subscription.contact)
        return mark_safe("<a href='{}'>{} {}</a>".format(url, subscription.contact.firstname, subscription.contact.lastname))

    contact_link.short_description = "Contact"
    fee_link.short_description = "Fee"

class SubscriptionInline(admin.TabularInline,AdminURLMixin):
    model = Subscription
    # fieldsets = [
    # (None, {'fields': ['fee', 'contacted']})
    # ] # list columns
    readonly_fields = ["created_at",'contacted', "fee_link"]

    def has_add_permission(self, request):
        return False

    def fee_link(self, subscription):
        path = "admin:store_fee_change"
        url = self.get_admin_url(subscription.fee)
        return mark_safe("<a href='{}'>{}</a>".format(url, subscription.fee.label))

    fee_link.short_description = "Fee"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    search_fields = ['firstname', 'lastname', 'email']
    inlines = [SubscriptionInline,] # list of bookings made by a contact
    extra=0

class FeeFeatureInline(admin.TabularInline):
    model = Fee.features.through # the query goes through an intermediate table.
    readonly_fields = ["feature_link"]
    extra = 1

    def feature_link(self, subscription):
        path = "admin:store_feature_change"
        url = self.get_admin_url(subscription.feature)
        return mark_safe("<a href='{}'>{}</a>".format(url, subscription.feature.label))

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass
    #inlines = [FeeFeatureInline,]

