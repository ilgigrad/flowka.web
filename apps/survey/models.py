from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagulous.models import TagField
from tag.models import TagSubject
from uuid import uuid1
from core.utils import format_html_lazy as format_html

# Create your models here.
class Survey2019(models.Model):
    TYPE= (
    (0, ''),
    (1,_('self employed')), #'Auto-entrepreneur
    (2,_('local administration')), #Collectivités locales
    (3,_('government')), #Collectivités régionales
    (4,_('education')), #Education
    (5,_('enterprise')), #Grande Entreprise
    (6,_('non-profit, non governmental organisation')), #ONG
    (7,_('small or medium business')), #PME/PMI
    (8,_('start-up')), #Startup
    (99,_('other...')), #Non applicable
    )

    ACTIVITY = (
        (0, ''),
        (1, _('wholesale distribution and retail trade')),
        (2, _('IT, digital, software, internet and telecom')),
        (3, _('bank, insurance or financial activities')),
        (4, _('industry and manufacturing')),
        (5, _('transportation, storage and logistic')),
        (6, _('construction, building, real estate')),
        (7, _('computers and electronics')), #Matériel informatique et électronique
        (8, _('research, science, environment')),
        (9, _('energy, electricity, gas, steam, water supply...')),
        (10, _('agriculture, forestry, fishing, mining')), #Agriculture, pêche, exploitation forestière et minière
        (11, _('legal, law')),
        (12, _('professional services')),
        (13, _('information, media, communication')),
        (14, _('cinema, arts, entertainment and gaming')),
        (15, _('sport, recreation, outdoor')),
        (16, _('travel, hospitality, accomodation, restaurant, food activities')),
        (17, _('healthcare and social work activities')),
        (18, _('education')),
        (19, _('public administration, government')),
        (20,_('non-profit organisation')),
        (99, _('other...')),
    )

    ROLE = (
        (0, ''),
        (1, _('liberal, partner, self employed')),
        (2, _('financial, accounting')),
        (3, _('IT/telecom')),
        (4, _('marketing, communication')),
        (5, _('sales')),
        (6, _('storage, logistic, supply-chain, transportation')),
        (7, _('human ressources')),
        (8, _('consultant, advisor')),
        (9, _('research, science academic')),
        (10, _('health, medical')),
        (11, _('journalist, media analyst')),
        (12, _('business executive, management, upper management')),
        (13, _('education')),
        (14, _('legal')),
        (15, _('buying, sourcing')),
        (16, _('technical, production')),
        (17, _('administration')),
        (18, _('developer, engineer')),
        (19, _('support services')),
        (20, _('entrepreneur')),
        (21, _('student')),
        (99, _('other...')),
    )

    FREQUENCY = (
        (0, ''),
        (200, _('daily')),
        (130, _('two or three times a week')),
        (50, _('weekly')),
        (30, _('two or three times a month')),
        (12, _('monthly')),
        (6, _('rarely')),
        (1, _('never')),
        )

    VISUALIZATION = (
        (0, ''),
        (1, _("I don't know")),
        (2, _('raw listings')),
        (3, _('columns tables')),
        (4, _('pivot tables')),
        (5, _('Olap hypercubes')),
        (6, _('graphs, curves or charts')),
        )

    TOOL = (
        (0, ''),
        (1, _("I don't know")),
        (2, _('none, a pocket calculator or pencil, rubber and paper...')),
        (3, _('Spreadsheet, Microsoft Excel, Google Sheets, Open Office Calc')),
        (4, _('Business Intelligence Desktop tools, Tableau, Qlik Sense, Sisense, Looker...')),
        (5, _('Business Intelligence enterprise reporting tools, SAP Business Objects, IBM Cognos, Microsoft Analysis Services/Power BI ')),
        (6, _('Enterprise Business Application or Package Software (SAP, PeopleSoft, Microsoft Dynamics, Cegid, Generix... )')),
        (7, _('Web\'s software as a service solution')),
        (8, _('IT specific reports')),
        (9, _('AI analysis, IBM Watson, Microsoft Azur Machine Learning...')),
        (10, _('developper tools, Python, Java, C#...')),
        (11, _('none of this...')),
        )

    STARS = (
        (0, _('not at all')),
        (1, _('not so much ')),
        (2, _('yes ')),
        (3, _('yes, very much')),
        (4, _('excellent')),
        )

    REVENUE = (
        (0, ''),
        (1, _('less than €1 Million')),
        (2, _('€1 Million to €10 Million')),
        (3, _('€10 Million to €100 Million')),
        (4, _('€100 Million to €500 Million')),
        (5, _('€500 Million to €1 Billion')),
        (6, _('over 1€ Billion')),
        )

    RECORDS = (
        (0, ''),
        (1, _('less than 1000')),
        (2, _('1000 to 9,999 (thousand)')),
        (3, _('10,000 to 99,999')),
        (4, _('100,000 to 1 Million')),
        (5, _('1 Million to 500 Million')),
        (6, _('over 500 Million')),
        )

    PRIVATE_ACTIVITY = (
        (0, ''),
        (1, _('sport')),
        (2, _('somehow scientific')),
        (3, _('managing an association')),
        (4, _('personal finance')),
        (5, _('pictures')),
        (6, _('cinema, music, some arts')),
        (7, _('social media')),
        (8, _('games, e-sport')),
        (9, _('bet, gambling, sport statistics')),
        (10, _('technologic, engine, personal IT')),
        (99, _('other..')),
        )

    PRIVATE_TOOL = (
        (0, ''),
        (1, _('none, a pocket calculator or pencil, rubber and paper...')),
        (2, _('Spreadsheet, Microsoft Excel, Google Sheets, Open Office Calc')),
        (3, _('Web\'s software as a service solution')),
        (4, _('some Apps (Strava, Runkeeper, Imdb, BetClic')),
        (99, _('others...')),
        )
    ip =  models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("IP address")
        )

    browser =  models.CharField(
            max_length=250,
            blank=True,
            null=True,
            verbose_name=_("client browser")
            )

    uid = models.CharField(max_length=36,null=True, blank=True, unique=True)

    uploaded_at = models.DateTimeField(
        verbose_name=_('uploaded at'),
        auto_now_add=True
        )

    type = models.IntegerField(
        blank=False,
        default=0,
        choices=TYPE,
        verbose_name=_('company type'),
        help_text= _('Select the type of company which is closer from the one you are working in...'),
        )

    type_other = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('specify type'),
        help_text= _('Could you, please, specify your company\'s type in the text field below'),
        )

    activity = models.IntegerField(
        blank=False,
        default=0,
        choices=ACTIVITY,
        verbose_name=_('company activity'),
        help_text= _('Select the main sector of the company/organization you are working in...'),
        )

    activity_other = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('specify activity'),
        help_text= _('Could you, please, specify  your company\'s activity in the text field below'),
        )

    revenue = models.IntegerField(
        blank=False,
        default=0,
        choices=REVENUE,
        verbose_name=_('company annual revenue'),
        help_text= _('Select the average annual revenue of your company. Leave empty if not allowed'),
        )

    role = models.IntegerField(
        blank=False,
        default=0,
        choices=ROLE,
        verbose_name=_('employee role'),
        help_text= _('What is your occupation or the department in which you work ?'),
        )

    role_other = models.CharField(
        default='',
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('specify occupation'),
        help_text= _('Could you, please, specify your occupation in the text field below.'),
        )

    has_data = models.BooleanField(
        blank=True,
        default=True,
        verbose_name=_('Are you dealing with data ?'),
        help_text= _('Check \'yes\' if your department is holding data (sales, logistic, clients, products details, technical data...)'),
        )

    frequency = models.IntegerField(
        blank=False,
        default=0,
        choices=FREQUENCY,
        verbose_name=_('analysis frequency'),
        help_text= _('How often are you analysing or building reports on those data ?'),
        )

    visualization = models.IntegerField(
        blank=False,
        default=0,
        choices=VISUALIZATION,
        verbose_name=_('reporting style'),
        help_text=format_html("{}<br>{}",
         _("How are you mainly visualizing your data ?"),
         _("What style of reporting are you dealing with ?")),
        )

    tool = models.IntegerField(
        blank=False,
        default=0,
        choices=TOOL,
        verbose_name=_('reporting tool'),
        help_text= _('What tool or software are you mainly using for building or looking at charts ?'),
        )

    can_extract= models.BooleanField(
        verbose_name=_('data extraction'),
        help_text=format_html("{}<br>{}",
         _("Are you sometimes extracting data out of the reporting tool you are using ?"),
         _("Check 'yes' if you use to export raw data out of the reporting tool to make analysis in a spreadsheets tool.")),
        default=False)

    reports = models.IntegerField(
        default=0,
        blank=False,
        )

    columns = models.IntegerField(
        default=5,
        blank=False,
        )

    lines = models.IntegerField(
        default=0,
        blank=False,
        )

    categories = models.IntegerField(
        default=0,
        blank=False,
        )

    records = models.IntegerField(
        blank=False,
        default=0,
        choices=RECORDS,
        verbose_name=_('Average number of records'),
        help_text= format_html("{}<br>{}<br><em>{}</em>",
            _("What is the size of datasets on which reports rely on ?"),
            _("e.g. a report that display informations over three weeks in 200 stores with an average of 50 sales a day,"),
            _(" ...the number of records will be 50 x 200 x 7 x 3 = 210,000"))
        )

    revenue = models.IntegerField(
        blank=False,
        default=0,
        choices=REVENUE,
        verbose_name=_('company annual revenue'),
        help_text= _('Select the average annual revenue of your company. Leave empty if not allowed.'),
        )

    private_activity = models.IntegerField(
        blank=False,
        default=0,
        choices=PRIVATE_ACTIVITY,
        verbose_name=_('Engaging in private activities ?'),
        help_text= format_html("{}{}",
            _("Whether it yield data you could analyze or not, are you involved in some private activities ?  "),
            _("From managing an association to training hard in some sports is there a specific activity in which you spend your free time ?")))

    private_tool = models.IntegerField(
        blank=False,
        default=0,
        choices=PRIVATE_TOOL,
        verbose_name=_('Analyzing private activities ?'),
        help_text= _("Is there any tool you use for that private activity ?")
        )


    company_keys = TagField(to=TagSubject,related_name='company')
    private_keys = TagField(to=TagSubject,related_name='private')

    company_description = models.TextField(null=True, blank=True, verbose_name=_('could you describe an IA use for your professional needs ?'))
    private_description = models.TextField(null=True, blank=True, verbose_name=_('could you describe an IA use for your private activities ?'))

    issues_description = models.TextField(null=True, blank=True, verbose_name=_('do you imagine some issues analysing data with IA tools ?'))

    is_analyst = models.BooleanField(
        verbose_name=_('Do you analyze your data yourself ?'),
        default=False,
        help_text= _("Do you often dive in your data to have a better understanding of underlying issues, rather than tracking the evolution of variables thru time ?"))

    is_dependant = models.BooleanField(
        verbose_name=_('Are you independant ?'),
        default=False,
        help_text=format_html("{}<br>{}",
            _("Check 'yes' if you do not feel highly dependant from others to access new sets of data."),
            _("If you do not rely on someone else's work and need to make a request to another department (e.g. IT) , consultants or a partner company and wait for a while before getting datasets or reports.")))

    has_mathematic = models.BooleanField(
        verbose_name=_('any mathematical background ?'),
        default=False,
        help_text=format_html("{}<br>{}",
            _("Do you have any mathematical backgrounds or some knowledge of mathematics and statistics that allow you to make advanced analysis of your data ?"),
            _("You master regression analysis (linear, polynomial or logistic) and many other heuristics and you know how to use them...")))

    has_scientist = models.BooleanField(
        verbose_name=_('data analysts around you?'),
        default=False,
        help_text=_("Do you have any data scientists or any dedicated team, easily approachable, in your working environment, with whom any Analysis question will have its answer in a few hours ? "))

    has_opendata = models.BooleanField(
        verbose_name=_("are you dealing with 'open data' ?"),
        default=False,
        help_text=_("Data freely provided by government or other organisations like traffic, meteo, train scheedules..."))

    anomaly = models.IntegerField( default=0, null=True, blank=True, verbose_name=_('anomaly detection ?'),choices=STARS)
    classif = models.IntegerField( default=0, null=True, blank=True, verbose_name=_('classification, automated categories assignment'),choices=STARS)
    predict = models.IntegerField( default=0, null=True, blank=True, verbose_name=_('predicting results'),choices=STARS)
    correl = models.IntegerField( default=0,  null=True, blank=True, verbose_name=_('finding correlation among your data, causality or links between events'),choices=STARS)
    segment = models.IntegerField( default=0, null=True, blank=True, verbose_name=_('segmentation, building relevant groups among your data'),choices=STARS)
    pict = models.IntegerField( default=0,  null=True, blank=True, verbose_name=_('picture categorization'),choices=STARS)
    text = models.IntegerField( default=0,  null=True, blank=True, verbose_name=_('text categorization'),choices=STARS)

    ai = models.IntegerField(
    default=0,
    null=True,
    blank=True,
    verbose_name=_('Artificial intelligence ?'),
    help_text=_("Wether you know who is HAL or not; What inspires you the concept of \"artificial intelligence\" ?"),
    choices=(
    (0, _("I don't know")),
    (1, _("it's science fiction only")),
    (2, _("it's a matter of huge company, self driving cars and big data")),
    (3, _('I would like to know how it can improve my business')),
    (4, _("I'm already engaged'")),
    ))

    ml = models.IntegerField( default=0,  null=True, blank=True,
    verbose_name=_('Machine learning ?'),
    help_text=_("have you already heard of \"machine learning\" ?"),
    choices=(
    (0, _("I don't know and I really don't care")),
    (1, _('Somehow a technical thing with computers and machines')),
    (2, _('It is related to education, like MOOCs, but machine are teaching')),
    (3, _('Obviously making prediction on some features by "training" a model with data'))
    ))

    smart = models.IntegerField( default=1,  null=True, blank=True,
    verbose_name=_('Smart data ?'),
    help_text=_("is \"smart data\" concept relevant to you ?"),
    choices=(
    (0, _("I don't want to know")),
    (1, _('it\'s like big data but comming from something smart')),
    (2, _('In my systems, data are not smart, it\'s only raw data')),
    (3, _('Less data but more relevant to have significant outputs and make decision'))
    ))

    pred = models.IntegerField( default=1,  null=True, blank=True,
    verbose_name=_('Predictions ?'),
    help_text=_("Do you believe in prediction given by some algorithms ?"),
    choices=(
    (0, _("I don't need that")),
    (1, _('I already can estimate outputs by myself')),
    (2, _('I won\'t be confident on prediction given by a machine')),
    (3, _('I would like to try on my own data'))
    ))

    email = models.EmailField(
        unique=False,
        null=True,
        help_text= _("We\'ll never share your email with anyone else..."),
        verbose_name=_('please, type your email address below if you wish to be informed of our activities, ')
        )

    def save(self,*args,**kwargs):
        if self.uid is None:
            self.uid=str(uuid1())
        super(Survey2019,self).save(*args,**kwargs)
