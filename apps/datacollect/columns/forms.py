from django import forms
from datacollect.models import DataSet
from .models import Column
from django.utils.translation import ugettext_lazy as _
from core.utils import format_html_lazy as format_html
from core.utils import get_code
from django.forms.widgets import NumberInput, Select, TextInput, CheckboxInput,HiddenInput,RadioSelect,CheckboxSelectMultiple
import json


def init_subform(object,module=''):
    if object.instance.alter == get_code(object.instance.ALTERS,module):
        try:
            rules=json.loads(object.instance.alter_rule)
            for key,value in rules.get(module,{}).items():
                field=object.fields.get(key,None)
                if field :
                    field.initial=value
        except:
            pass

class ColumnForm(forms.ModelForm):
    """
    get parameters for cleaning
    """
    class Meta:
        model = Column
        fields = ('id', 'rename','drop_column','target','alter','nan','category', 'outliers')

    rename=forms.CharField(
        widget=TextInput(),
        required=False,
        label=_("rename this column"),
        help_text=_("type a new name for the column"))

    drop_column=forms.BooleanField(
        widget=CheckboxInput(),
        initial=False,
        label=_("drop column"),
        help_text=_("drop this column"))

    outliers=forms.BooleanField(
        widget=CheckboxInput(),
        initial=False,
        label=_("drop outliers"),
        help_text=_("set a filter on values that are out of a standard range for this dataset"))

    target=forms.BooleanField(
        widget=CheckboxInput(),
        initial=False,
        label=_("set as target"),
        help_text=_("select this column as a target for prediction or classification"))

    alter = forms.IntegerField(
        widget=RadioSelect(choices=[(x[0],x[1]) for x in  Column.ALTERS],attrs={'choices': Column.ALTERS[1:]}),
        initial=0,
        label=_('field transformation'),
        help_text= format_html("{} {}",
            _("Do you need to transform this field and how would you transform it ?"),
            _("Transform string to number or time format, extract a substring..."))
        )

    alter_rule = forms.CharField(required=False,widget=HiddenInput())
    nan_rule = forms.CharField(required=False,widget=HiddenInput())
    # alter_rule=forms.CharField(
    #     widget=TextInput(),
    #     required=False,
    #     label=_('field transformation rule'),
    #     help_text=_("Please, Specify the rule"))

    nan=forms.IntegerField(
        widget=RadioSelect(choices=[(x[0],x[1]) for x in  Column.NANS],attrs={'choices': Column.NANS[1:]}),
        initial=0,
        label=_('managing missing values'),
        help_text= format_html("{}<br>{}",
            _("What do you want to do when values are missing ?"),
            _("Drop rows with none values or set a rule for replacing them them."))
        )

    # nan_rule=forms.CharField(
    #     widget=TextInput(),
    #     required=False,
    #     label=_("please specify a value"))

    category=forms.IntegerField(
        widget=RadioSelect(choices=[(x[0],x[1]) for x in  Column.CATEGORIES],attrs={'choices': Column.CATEGORIES[1:]}),
        initial=0,
        label=_('managing categories'),
        help_text= format_html("{}<br>{}",
            _("How would you manage category values ?"),
            _("Category is often non numerical like a country or a color..."))
        )


    def clean(self):
        cleaned_data = super().clean()
        target = cleaned_data.get("target")
        drop = cleaned_data.get("drop_column")

        if drop and target:
            # Only do something if both fields are valid so far.
            raise forms.ValidationError(
                _("a target Column should not be droped")
            )

class SplitColumnForm(forms.ModelForm):
    class Meta:
        model=Column
        fields=('spliter','substrings',)

    SSTRINGS=[(x,'{:02d}'.format(x)) for x in range(10)]
    spliter=forms.CharField(initial='', label=_("split characters"), help_text=_("characters used for splitting the string in substrings"))

    substrings=forms.MultipleChoiceField(
        required=False,
        choices=SSTRINGS,
        widget=CheckboxSelectMultiple())

    def __init__(self,*args,**kwargs):
        super(SplitColumnForm,self).__init__(*args,**kwargs)
        init_subform(self,'splitize')

class SubstrColumnForm(forms.ModelForm):

    class Meta:
        model=Column
        fields=('substrer','substrings',)

    substrer=forms.MultipleChoiceField(
        required=False,
        choices=[1,2,3],
        widget=CheckboxSelectMultiple())

    SSTRINGS=[(x,'{:02d}'.format(x)) for x in range(10)]

    substrings=forms.MultipleChoiceField(
        required=False,
        choices=SSTRINGS,
        widget=CheckboxSelectMultiple())

    def __init__(self,*args,**kwargs):
        super(SubstrColumnForm,self).__init__(*args,**kwargs)
        init_subform(self,'substrize')
        import ipdb; ipdb.set_trace()


class RegexColumnForm(forms.ModelForm):
    class Meta:
        model=Column
        fields=('regex',)

    regex=forms.CharField(initial='', label=_("regular expression"), help_text=_("use a regular expression to create substrings"))

    def __init__(self,*args,**kwargs):
        super(RegexColumnForm,self).__init__(*args,**kwargs)
        init_subform(self,'regex')

# %Y year 4
# %y year 2
# %m month 01-12
# %n month 1-12
# %b Month as locale’s abbreviated name
# %B Month as locale’s full name.
# %U week number (start sunday)
# %W week number (start monday)
# %d day of the month 01-31
# %j day of the year
# %w day of the week number
# %a day of the week short
# %A day of the week long
# %H hour 24
# %I hour 12
# %p AM PM
# %M minutes
# %S seconds
# %f microsecond
# %Z Time zone name
# %z UTC
# %c local date and times
# %x local version time
# %X local version date
# %% % character

class TimeColumnForm(forms.ModelForm):
    TIMEFORMAT={
    (0,"personalize","personalize"),
    (1,"%Y-%m-%d","2018-09-21"),
    (2,"%Y-%b-%d","2018-sep-21"),
    (3,"%Y-%B-%d","2018-september-21"),
    (4,"%y-%m-%d","18-09-21"),
    (5,"%m-%d-%Y","09-21-2018"),
    (6,"%b-%d-%Y","sep-21-2018"),
    (7,"%B-%d-%Y","september-21-2018"),
    (8,"%m-%d-%y","09-21-99"),
    (10,"%Y-%m-%dT%H:%M","2018-09-21T20:06"),
    (11,"%Y-%m-%dT%H:%M:%S","2018-09-21T20:06:57"),
    (12,"%Y-%m-%dT%H:%M:%S.%f","2018-09-21T20:06:57.000"),
    (13,"%Y-%m-%dT%H:%M:%S.%f%Z","2018-09-21T20:06:57.000[Europe/Paris]"),
    (14,"%Y-%m-%dT%H:%M:%S.%f%z","2018-09-21T20:06:57.000+01:00"),
    (15,"%Y-%m-%dT%H:%M:%S%z","2018-09-21T20:06:57+01:00"),
    (16,"%Y-%m-%dT%H:%M%z","2018-09-21T20:06+01:00"),
    (20,"%Y-%j","2018-264"),
    (21,"%Y-%W-%w","2018-38-5"),
    (22,"%Y-%W-%a","2018-38-Fri"),
    (23,"%Y-%W-%A","2018-38-Friday"),
    (30,"%d-%m-%Y","21-09-2018"),
    (31,"%d-%b-%Y","21-sep-2018"),
    (32,"%d-%B-%Y","21-september-2018"),
    (33,"%d-%m-%y","18-09-21"),
    (40,"%d-%m-%YT%H:%M","21-09-2018T20:06"),
    (41,"%H:%M:%S","20:06:57"),
    (42,"%H:%M:%S.%f","20:06:57.111"),
    (43,"%I:%M:%S","08:06:57"),
    (44,"%I:%M:%S %p","08:06:57 PM")}

    TIMES={("datetime",_("full date and time"),_("keep full date and time informations")),
    ("date",_("full date"),_("keep date informations")),
    ("time",_("full time"),_("keep time informations")),
    ("years",_("years"),_("keep years")),
    ("months",_("months"),_("keep months")),
    ("weeks",_("weeks"),_("keep weeks")),
    ("weekdays",_("weekdays"),_("keep weekdays")),
    ("days",_("days"),_("keep days")),
    ("hours",_("hours"),_("keep hours")),
    ("minutes",_("minutes"),_("keep minutes")),
    ("seconds",_("seconds"),_("keep seconds"))}

    class Meta:
        model=Column
        fields=('dt_format','timeselect',)

    dt_format=forms.IntegerField(
        widget=Select(choices=[(x[0],'{}...{}'.format(x[1],x[2])) for x in TIMEFORMAT]),
        initial=0,
        label=_('time format'),
        help_text= format_html("{} {}",
            _("Select the format of your date/time string;"),
            _("Any separators will match"))
        )


    timeselect=forms.MultipleChoiceField(
        required=False,
        choices=[(x[0],x[1]) for x in TIMES],
        widget=CheckboxSelectMultiple(
        attrs={'choices': TIMES}))


    def __init__(self,*args,**kwargs):
        super(TimeColumnForm,self).__init__(*args,**kwargs)
        init_subform(self,'timize')
