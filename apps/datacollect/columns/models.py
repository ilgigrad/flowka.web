from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.utils.text import slugify
from core.utils import LazyEncoder
from datacollect.models import DataSet
from .managers import ColumnManager


class Column(models.Model):

    objects = ColumnManager()

    class Meta:
        verbose_name = 'column'
        verbose_name_plural = 'columns'


    ALTERS = (
        (0, 'unchanged',_('No Transform '), _('Leave field unchanged'),False,''),
        (1, 'intize',_('Integer'),_('Transform string numeric values or truncate decimals into integers'),False,''),
        (2, 'floatize', _('Decimal'),_('Transform string numeric values or int into floats'),False,''),
        (3, 'timize',_('Time'),_('Select a time or date format for this field'),True,'/datacollect/timecolumn/'),
        (4, 'splitize', _('Split'),_('Split a field with a separator and create new columns'),True, '/datacollect/splitcolumn/'),
        (5, 'substrize', _('Substring'),_('Split a field with position and create new columns from those substrings'),True, '/datacollect/substrcolumn/'),
        (6, 'regexize', _('Regex'),_('Split a field based on a regular expression and create new columns'),True, '/datacollect/regexcolumn/')
        )

    NANS = (
        (0, 'leave',_('Leave NANS'),_('Leave empty, none or null values unchanged'),False,''),
        (1, 'drop', _('Drop rows'),_('Drop rows which contain missing values on that column'),False,''),
        (2, 'binary', _('Binary'),_('Replace missings by -False- and other values by -True-'),False,''),
        (3, 'median', _('Median'),_('Replace missings by the median value in the column'),False,''),
        (4, 'mean', _('Mean'),_('Replace missings by the mean value in the column'),False,''),
        (5, 'highfreq', _('highest frequency'),_('Replace missings by the value that appears with the highest frequency'),False,''),
        (6, 'lowfreq', _('lowest frequency'),_('Replace missings by the value that appears with the lowest frequency'),False,''),
        (7, 'max', _('Max'),_('Replace missings by the maximum value of the column'),False,''),
        (8, 'min', _('Min'),_('Replace missings by the minimum value of the column'),False,''),
        (9, 'value', _('Value'),_('Replace missing by a specific value'),True,'/datacollect/timecolumn/')
        )



    CATEGORIES = (
        (0, 'keep', _('Keep'),_('Leave categories unchanged'),False,''),
        (1, 'dummelies', _('Dummies'),_('Each distinct value become a new column'),False,''),
        (2, 'frequencies', _('Frequencies'),_('Replace each value by it\\\'s frequency in the column'),False,''),
        (3, 'ordinals', _('Ordinals'),_('Values are ordered and ranked'),False,'')
        )
    dataset=models.ForeignKey(DataSet, on_delete=models.CASCADE)
    initial=models.CharField(blank=True, null=True, default='',max_length=100, verbose_name=_('column'), help_text=_('column title'))
    slug=models.CharField(blank=True, null=True, default='',max_length=100, verbose_name=_('slug'), help_text=_('slug'))
    rename=models.CharField(blank=True, null=True,max_length=100, verbose_name=_("rename this column"), help_text=_("type a new name for the column"))
    drop_column=models.BooleanField(default=False, verbose_name=_("drop column"), help_text=_("drop this column ?"))
    outliers=models.BooleanField(default=False, verbose_name=_("drop outliers"), help_text=_("set a filter on values that are out of a standard range for this dataset"))
    target=models.BooleanField(default=False, verbose_name=_("set as target"), help_text=_("is this column a target for prediction or classification ?"))

    alter = models.IntegerField(
        blank=False,
        default=0,
        choices=[(x[0],x[1]) for x in ALTERS],
        verbose_name=_('field transformation'),
        help_text= format_html("{}<br>{}",
            _("Do you need to transform this field and how would you transform it ?"),
            _("transform string to number or time format, extract a substring or set a \"regex\" rule"))
        )

    alter_rule=models.CharField(
        blank=True,
        null=True,
        default='',
        max_length=255,
        verbose_name=_('field transformation rule'),
        help_text=_("Please, Specify the rule"))

    nan=models.IntegerField(
        blank=False,
        default=0,
        choices=[(x[0],x[1]) for x in NANS],
        verbose_name=_('managing missing values'),
        help_text= format_html("{}<br>{}<br>{}",
            _("What do you want to do when values are missing ?"),
            _("Drop rows with none values or set a rule for replacing them them."),
            _("e.g. use statistics indicators (median, mean, max...) in place of missing values"))
        )

    nan_rule=models.CharField(
        blank=True,
        null=True,
        default='',
        max_length=255,
        verbose_name=_("please specify a value"))

    category=models.IntegerField(
        blank=False,
        default=0,
        choices=[(x[0],x[1]) for x in CATEGORIES],
        verbose_name=_('managing categories'),
        help_text= format_html("{}<br>{}<br>{}",
            _("How would you manage category values ?"),
            _("Category is a non numerical value that can not be computed (sum, mean,... )"),
            _("it is often a text field like country or color..."))
        )


    def __str__(self):
        return '{} / {} / {}'.format(self.id,self.slug,self.initial)

    def __init__(self,*args,**kwargs):
        #import ipdb; ipdb.set_trace()
        initial=kwargs.pop('initial',None)
        super(Column,self).__init__(*args,**kwargs)
        if initial:
            self.initial=initial
        self.slug=slugify(self.initial)
        if not self.rename:
            self.rename=self.initial


    def save(self,*args,**kwargs):
        Column.objects.onetarget(self)
        super(Column,self).save(*args,**kwargs)


    @property
    def to_json(self):
        from django.core import serializers
        serializers.serialize('json',[f,])
        return serializers.serialize('json',[f,])
