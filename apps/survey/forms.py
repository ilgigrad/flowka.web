from django import forms
from survey.models import Survey2019
from django.utils.translation import ugettext_lazy as _
from tagulous.forms import TagField
from tag.models import TagSubject
from tagulous.models import TagOptions
from core.custom_forms_fields import ExtEmailField
from django.forms.widgets import NumberInput,RadioSelect
from core.utils import format_html_lazy as format_html





class Survey2019Form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(Survey2019Form,self).__init__(*args,**kwargs)
        self.fields['activity_other'].strip=False
        self.fields['role_other'].strip=False
        self.fields['type_other'].strip=False
        self.fields.keyOrder = ['type','type_other','activity','activity_other','role','role_other','revenue',
            'company_keys','company_description',
            'has_data','visualization','tool','can_extract',
            'frequency','reports','columns','lines','categories', 'records',
            'is_analyst','is_dependant','has_mathematic','has_scientist',
            'predict','classif','segment','correl','anomaly','pict', 'text',
            'ai','ml','smart','pred','has_opendata',
            'private_activity','private_tool','private_keys','private_description',
            'issues_description','email']

    class Meta:
        model = Survey2019
        fields = ('type','type_other','activity','activity_other','role','role_other','revenue',
            'company_keys','company_description','has_opendata',
            'has_data','visualization','tool','can_extract',
            'frequency','reports','columns','lines','categories', 'records',
            'is_analyst','is_dependant','has_mathematic','has_scientist',
            'predict','classif','segment','correl','anomaly','pict', 'text',
            'ai','ml','smart','pred','has_opendata',
            'private_activity','private_tool','private_keys','private_description',
            'issues_description','email',)


    company_keys=TagField(
        required=False,
        tag_options=TagOptions(
        force_lowercase=True,
        ),
        autocomplete_tags=TagSubject.objects.autocomplete_most_frequent(),
        label=_('Tag your KPI'),
        help_text=format_html("{}<br>{}<br>{}<br>{}",
            _("Tag the name of your main indicators or dimensions."),
            _("Type any key that is important in your reports."),
            _("For exemple : age, country, revenue, speed, timeout, quantity..."),
            _("Use blank to split words and use double quotes to join words in a \"same tag\"")))

    company_description = forms.CharField(
        #label='description',
        max_length=1000,
        widget=forms.Textarea(attrs={'type':'textarea','placeholder': _('Describe here your professional need for IA reports, if any...'), 'id':'id_company_description','onkeyup':"textCount(this);",'resize':'none', 'class':'w-100'}),
        required=False,
        label=_("IA for your business ?"),
        help_text=format_html("{}<br>{}<br>{}",
            _("What are your expectations for IA tools in your business ?"),
            _("What could you expect of a machine learning tool for improving your business analysis ?"),
            _("If you \"own\" already such a tool, what are the lacks you wish to overcome ?")))

    reports = forms.IntegerField(
        label=_('Reports'),
        help_text= _('What is the average number of distinct reports or charts are you usually browsing ?'),
        widget=NumberInput(attrs={'type':'range', 'min':'0', 'max':'100', 'step':'1'}),
        initial=0)

    columns = forms.IntegerField(
        label=_('Indicators'),
        help_text= _("What is the average number of columns, indicators or KPI, contained in your reports ?"),
        widget=NumberInput(attrs={'type':'range', 'min':'0', 'max':'200', 'step':'2'}),
        initial=0)

    lines = forms.IntegerField(
        label=_('Lines'),
        help_text=format_html("{}<br>{}",
         _("What is the average number of lines contained in your reports ?"),
         _("Wether it's sorted by products services, departments or some geographics area, how many rows is there in your reports ?")),
        widget=NumberInput(attrs={'type':'range', 'step': '1', 'min':'0', 'max':'500', 'step':'5'}),
        initial=0
        )

    categories = forms.IntegerField(
        label=_('Categories'),
        help_text= format_html("{}<br>{}<br>{}<br>{}",
            _("What is the average number of categories or dimensions in your reports ?"),
            _("Categories are mostly not numeric data."),
            _("They can't be computed but provide qualitative informations."),
            _(" For exemple : geographic areas, colors or groups of products...")),
        widget=NumberInput(attrs={'type':'range', 'min':'0', 'max':'100', 'step':'1'}),
        initial=0
        )

    predict = forms.IntegerField(
        widget=NumberInput(attrs={'type':'rating'}),
        required=False,
        label=_('Making predictions'),
        initial=0,
        help_text= format_html("{}<br>{}<br>{}",
        _("How interested are you in building predictions out of your data ?"),
        _("Predictions can be any numerical value like a price, a cost, an quantityt of stock, a distance or a speed..."),
        _("It allows to make estimations based on the relationships between variables which are more accurate than any \"human guesses\"")))

    classif = forms.IntegerField(
        widget=NumberInput(attrs={'type':'rating'}),
        required=False,
        label=_('Making classification'),
        initial=0,
        help_text= format_html("{}<br>{}<br>{}<br>{}<br><strong>{}</strong>",
        _("Classification models identify which category an observation belongs to. It rely on previous data to learn how to affect a set of inputs to a \"class\"."),
        _("classification could be binary (e.g. is a customer going to churn ? will this person repay a loan ?)"),
        _("...or refers to multiclass (e.g. which of this four chanels could be more efficient for that product ? )"),
        _("Results are then analyzed with Matrix confusion"),
        _("(True:Positive/Negative - False:Positive/Negative )")))

    segment = forms.IntegerField(
        widget=NumberInput(attrs={'type':'rating'}),
            required=False,
            label=_('Building clusters'),
            initial=0,
            help_text=format_html("{}<br>{}<br>{}",
            _("Clusterization is building groups of similar data."),
            _("You specify the number of groups you want to create and data are automaticaly distributed over those groups."),
            _("It allows to create sets of clients, products or any items, based on every inputs and not few categories like it used to be.")))

    correl = forms.IntegerField(
        widget=NumberInput(attrs={'type':'rating'}),
        required=False,
        label=_('Finding Correlations'),
        initial=0,
        help_text=format_html("{}<br>{}",
        _("Finding Correlations reveals what are the links between your data and what is the strength of those links."),
        _("Some correlations may be obvious but some could be surprizing as it becomes very hard to figure out how data correlates if you have more than two features.")))

    anomaly = forms.IntegerField(
        widget=NumberInput(attrs={'type':'rating'}),
        required=False,
        label=_('Anomaly detection'),
        initial=0,
        help_text=format_html("{}<br>{}",
        _("Detecting outliers or unusal patterns in your data allow to detect anomalies or frauds in your systems."),
        _("Log files can be analysed as well as any technical informations.")))

    pict = forms.IntegerField(
        widget=NumberInput(attrs={'type':'rating'}),
        required=False,
        label=_('Image recognition'),
        initial=0,
        help_text=format_html("{}<br>{}",
        _("Training the machine to find features and associate appropriate tags to your picture."),
        _("Automatic detection of colours, items (e.g. bag, glasses, dress, bike...), faces, landscapes (e.g. beach, mountain, city...) or even situations.")))

    text = forms.IntegerField(
        widget=NumberInput(attrs={'type':'rating'}),
        required=False,
        label=_('Text mining'),
        initial=0,
        help_text=_("Text mining opens door to Sentiment Analysis (how a writer feels or reacts), keywords extraction or summarization, or entity recognition (identifying dates, places, names, organizations...)"))


    ai = forms.IntegerField(widget=RadioSelect(
    attrs={'type':'radio'},
    choices=(
    (0, _("I don't know")),
    (1, _("it's science fiction only")),
    (2, _("it's a matter of huge company, self driving cars and big data")),
    (3, _('I would like to know how it can improve my business')),
    (4, _("We are already engaged in AI")),
    )),
    label=_('Artificial intelligence ?'),
    initial=0,
    help_text=format_html("{}<br>{}",
        _("Wether you are vey involved in data science or not, what inspires you the concept of \"artificial intelligence\" ?"),
        _("How closed are you from using such technologies in your business or for some private analysis ?")),
    required=False)

    ml = forms.IntegerField(widget=RadioSelect(
    attrs={'type':'radio'},
    choices=(
    (0, _("I don't know")),
    (1, _("Reports depend mainly on acounting data")),
    (2, _("Most operational and raw data are followed up")),
    (3, _("We are managing big data and every single data is exploited"))
    )),
    help_text=format_html("{}<br>{}<br>{}",
        _("Most systems store huge amounts of data that are not used in business analysis."),
        _("e.g. Emails and customers informations are mainly quarried for mailing promotions and newsletters but rarely for building classifications or some predictions."),
        _("Are you mining informations about your business health in your whole database or just on few indicators as margin, cost and revenue ?")),
    label=_('Wasting data ?'),
    initial=0,
    required=False)

    smart = forms.IntegerField(widget=RadioSelect(
    attrs={'type':'radio'},
    choices=(
    (0, _("I don't know")),
    (1, _('I can easily take decisions by watching my reports')),
    (2, _('Reports are just giving a kind of \"humor\" about the business.')),
    (3, _('There are absolutely no links between data and decisions.'))
    )),
    label=_('Smart data ?'),
    initial=0,
    help_text=format_html("{}<br>{}<br>{}",
    _("\"Smart Data\" is a concept that leads to analyze less data but that are more accurate."),
    _("It's quite different from big data which involves huge quantities of data, from text to pictures or videos."),
    _("How close do you think your data are from beeing smart ?"),),
    required=False)

    pred = forms.IntegerField(widget=RadioSelect(
    attrs={'type':'radio'},
    choices=(
    (0, _("I don't know")),
    (1, _("I don't need to predict anything")),
    (2, _('I already can estimate outputs by myself')),
    (3, _('I won\'t be confident on prediction given by a machine')),
    (4, _('I would like to try on my own data'))
    )),
    label=_('Predictions ?'),
    initial=0,
    help_text=_("Regarding your data, are you just watching at them or are you able to make some prediction on what could happened ?"),
    required=False)


    private_keys=TagField(
        required=False,
        tag_options=TagOptions(
        force_lowercase=True,
        ),
        autocomplete_tags=TagSubject.objects.autocomplete_most_frequent(),
            label=_('Tag your private KPI'),
            help_text=format_html("{}<br>{}<br>{}<br>{}",
                _("Tag the name of the elements you would like to analyse."),
                _("Type any key, dimension or indicator that could appears in your private interests"),
                _("For exemple : pace, speed, time, run, travel, cost..."),
                _("Use blank to split words and use double quotes to join words in a \"same tag\"")))

    private_description = forms.CharField(
        #label='description',
        max_length=1000,
        widget=forms.Textarea(attrs={'type':'textarea','placeholder': _('type your text here...'), 'id':'id_private_description','onkeyup':"textCount(this);",'resize':'none', 'class':'w-100'}),
        required=False,
        label=_('IA for private data ?'),
        help_text=format_html("{}<br>{}<br>{}<br>{}",
            _("Do you have any expectations for a IA tool for private data or activities ?"),
            _("Describe your private  need for IA reports, if any..."),
            _("What could you expect of a machine learning tool in a private use ?"),
            _("If you \"own\" already such a tool, what are the lacks you wish to overcome ?")))

    issues_description = forms.CharField(
            #label='description',
        max_length=1000,
        widget=forms.Textarea(attrs={'type':'textarea','placeholder': _('Comment possible issues of IA analysis'), 'id':'id_issues_description','onkeyup':"textCount(this);",'resize':'none', 'class':'w-100'}),
        required=False,
        label=_('Suspecting issues ?'),
        help_text=format_html("{}<br>{}",
            _("Are you suspecting machine learning to bring issues ?"),
            _("Do you have any about a dark side of such tools ?")))

    email = ExtEmailField(
        label=_('Thank You !'),
        max_length=200,
        widget=forms.EmailInput(attrs={ 'placeholder':_('type your email here')}),
        required=False,
        help_text= format_html("{}<br>{}",
        _("(optional) Type your email address below if you wish to be informed of our activities."),
        _("We\'ll never share your email with anyone else...")))
