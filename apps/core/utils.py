from datetime import datetime as dt
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.conf import settings
import re
from django.utils.deconstruct import deconstructible
import os, time, uuid
from django_currentuser.middleware import get_current_user
from django.utils.functional import lazy
from django.utils.html import format_html


format_html_lazy = lazy(format_html, str)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_form_errors_list(errors):
    """
    return a list of error descs without the key
    """
    errors_list=[]
    for errorKey,errorDesc in errors.items():
        errors_list.append(errorDesc)
    return errors_list


def size_prefix(size,precision=3,bytes=True,short=True):
    """
    return a file size or dimension with apropriate prefix range
    bytes :
        True for bytes(1kb=2⁽¹⁰⁾b=1024b)
        False for dims like rows or columns length : (1k=10³)
    """
    range={True:1024.0,False:1000.0}[bytes]
    shortPrefixes=['','k','M','G','T','P','E','Z','Y']
    longPrefixes=['','kilo','Mega','Giga','Tera','Peta','Exa','Zetta','Yotta']
    prefixes={True:shortPrefixes, False:longPrefixes}[short]
    prefixIndex = 0

    while size > range and prefixIndex < 9:
        prefixIndex += 1 #increment the index of the suffix
        size = size/range #apply the division
    return "%.*f%s"%(precision,size,prefixes[prefixIndex])


def shortdate(datetime):
    """
        display wether the time xor the date depending on date is today or not
    """
    today=dt.now().date()
    shortdate=datetime.date()
    if today==shortdate:
        return datetime.time()
    else:
        return shortdate

def str_to_bool(value):
    """
    convert string containing a boolean to boolean
    """
    valid=["true","yes","1"]

    if isinstance(value, bool):
        return value
    elif isinstance (value, int):
        return value==1
    elif not isinstance(value, str):
        raise ValueError(_('invalid literal for boolean. Not a string.'))
    elif value.lower() in valid:
        return True
    else:
        return False

def toStr(obj):
    """
    convert list or int to str. str remains str
    """
    if isinstance(obj,str):
        return obj
    elif isinstance(obj,list):
        return ','.join(obj)
    elif isinstance(obj,int) or isinstance(obj,float) or isinstance(obj,bool):
        return str(obj)

def toInt(obj):
    """
    convert str, float or even int to int
    """
    if isinstance(obj,str) and obj.isdigit():
        return int(obj)
    elif isinstance(obj,float):
        return int(obj)
    elif isinstance(obj,int) :
        return obj
    else:
        return 0


def listIfNot(obj):
    """
        if oject is not a list, transform it in a list of unique element
    """
    if not isinstance(obj,list):
        return [obj]
    return obj

class Const:

    COLOR={'prune':'#615375','lightprune':'#796989','rose':'#fed4e0','apricot':'#f9bf76',
        'anis':'#dedd23','electric':'#34a9d4','sadsea':'#72b2c5','peach':'#e5625c',
        'blood':'#d1313d','gray':'#686f76','dark':'#3d464f','white':'#fff',
        'black':'#000'}

    ICON={'c-question':'fal fa-question-circle',
            'c-down':'fal fa-arrow-alt-circle-down',
            'c-plus':'fal fa-plus-circle',
            'c-minus':'fal² fa-minus-circle',
            'c-play':'fal fa-play-circle',
            'c-check':'fal fa-check-circle',
            'c-exclamation':'fal fa-exclamation-circle',
            'c-dot':'fal fa-dot-circle',
            'c-invalid':'fal fa-times-circle',
            'c-empty':'fal fa-circle',
            'c-plus-solid':'fas fa-plus-circle',
            'crown':'fal fa-crown',
            'folder':'fal fa-folder',
            'folders':'fal fa-folders',
            'folder-plus':'fal fa-folder-plus',
            'folder-minus':'fal fa-folder-minus',
            'star':'fal fa-star',
            'share':'fal fa-share',
            's-plus':'fal fa-plus-square',
            's-minus':'fal fa-minus-square',
            'expand':'fal fa-expand',
            'share-alt':'fal fa-share-alt',
            'world': 'fal fa-globe-europe',
            'image': 'fal fa-images',
            'images': 'fal fa-image',
            'terminal': 'fal fa-terminal',
            'back': 'fal fa-arrow-to-left',
            }

def set_sites(newsite=None):
    """
    insert sites names and domains in database
    """
    from django.contrib.sites.models import Site
    sites = ['flowka.com','ilgigrad.net']
    if newsite is not None:
        sites+=listIfNot[newsite]
    for site in sites:
        Site.objects.get_or_create(name=site,domain=site)

    return Site.objects.all().values_list('id','domain')

def parse_args(expected,*args,**kwargs):
    """
        parse args and kwargs within an expected dict
    """
    if not isinstance(expected,dict):
        try:
            arg_l=dict(expected)
        except:
            return {}
    else:
        arg_l=expected #expected should be a dict
    #retrieve the arguments list
    keys=list(arg_l.keys())
    for i,key in enumerate(keys):
        if i<len(args):
            arg_l[key]=args[i]
        arg_l[key]=kwargs.get(key,arg_l[key])
    return arg_l


def paginator(items,itemsPerPage,page):
    paginator = Paginator(items,itemsPerPage)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    return items, paginator.num_pages>1

def get_session(request,label):
    if hasattr(request, 'session'):
        return request.session.get(label,{})
    else:
        return {}


@deconstructible
class PathAndRename(object):

    def __init__(self,sub_path=None,prefix=None):
        self.path = sub_path
        self.prefix=prefix

    def __call__(self,instance,filename):
        # eg: filename = 'my uploaded file.jpg'
        ext = filename.split('.')[-1]  #eg: 'jpg'
        uid = uuid.uuid4().hex[:5]    #eg: '567ae32f97'
        date= time.strftime('%Y%m%d')
        user=get_current_user()
        if user:
            userpk = user.pk
        else:
            # eg: 'my-uploaded-file'
            userpk = ''
        if self.prefix==None:
            prefix=""
        else:
            prefix="%(prefix)_" % {'prefix':self.prefix}
        # eg: 'my-uploaded-file_64c942aa64.jpg'
        renamed_filename = '%(prefix)s%(userpk)s_%(date)s_%(uid)s.%(ext)s' % {'prefix':prefix,'userpk': userpk, 'date':date,'uid': uid, 'ext': ext.lower()}
        #

        file=['xls','xlsx','html','htm','txt','csv','json','xml','log']
        img=['jpeg','jpg','bmp','tiff','gif','png',]
        if ext.lower() in file:
            self.path="files/"
        elif ext.lower() in img:
            self.path="photos/"
        else:
            self.path="bin/"

        # eg: 'avatar/my-uploaded-file_64c942aa64.jpg'
        return os.path.join(self.path, renamed_filename)




def is_image(file):

    from mimetypes import guess_type
    imgRegex=r'image'
    imgExt=['jpg','jpeg','png','tiff']
    try:
        match = re.search(imgRegex,guess_type(file.name)[0])
    except:
        return False
    if file.name.lower().split('.')[-1] in imgExt and match:
        return True
    return False


def is_data(file):
    from mimetypes import guess_type
    fileRegex=r'text|xls|ods|xml|json|excel|spreadsheet'
    fileExt=['txt','xls','ods','xml','json','htm','html','rtf','csv','log','xlsx']
    try:
        match = re.search(fileRegex,guess_type(file.name)[0])
    except:
        return False
    if file.name.lower().split('.')[-1] in fileExt and match:
        return True
    return False

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def dict_invert(adict):
    #invert a dictionary that represents ligs and cols
    cols=list(adict.keys())
    ligs=list(adict[cols[0]].keys())
    inv={lig:{col:adict[col][lig] for col in cols} for lig in ligs}
    return inv



from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)

def get_code(tuple,label):
    return { x[1]:x[0] for x in tuple }.get(label,None) 
