from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagulous.models import TagTreeModel
from core.utils import parse_args


class TagManager(models.Manager):

    def autocomplete_most_frequent(self):
        return self.all().order_by('-count','-id').values_list('name',flat=True)[:1000]

class TagSubject(TagTreeModel):
    class TagMeta:
        initial = [
        _('retail'),
        _('correlation'),
        _('production'),
        _('learning'),
        _('retail/sales'),
        _('retail/stocks'),
        _('customers'),
        _('CRM'),
        _('business'),
        _('HR'),
        _('legal'),
        _('IT'),
        ]
        force_lowercase = True
        max_count=15
        autocomplete_view = 'tag:tag_subject_autocomplete'
        autocomplete_initial=True

    objects=TagManager()


def search_by_tags (*args,**kwargs):
    """
        strict=False,cls=None,column='',related=None,searchTags=[],user=None
        a function that allows to search on a list of searchTags for tags of an object
        ie: search_by_tags(True,Files,'subjects',['it','data science','statistics'],user)
        or  strict_in(UserProfile,'interests__name','contains',['it','math','ski','trail'])
    """
    arg_l={
        'user':None,
        'cls':None,
        'column':'',
        'related':None,
        'strict':False,
        'searchTags':[],
        }

    #retrieve the arguments list
    arg_l=parse_args(arg_l,*args,**kwargs) #fill d with args and kwargs or dict d if no args
    #import ipdb; ipdb.set_trace()
    # search objects on tags list
    query_tag = arg_l['cls'].objects
    if arg_l['strict']: #tags=foo & tags=bar
        myfilter = arg_l['column']
        for value in arg_l['searchTags']:
            query_tag=query_tag.filter(**{myfilter:value})
    elif len(arg_l['searchTags'])>0: #tags_in=[foo,bar]
        myfilter = arg_l['column']+'__name__in'
        query_tag=query_tag.filter(**{myfilter:arg_l['searchTags']})
    else: #searchTags=[] => no filter
        pass #implicitly query_tag=query_tag.all()

    #filter with perms
    query_public=query_tag.filter(is_public=True) #public objs
    if arg_l['user'] is not None:
        query_user=query_tag.filter(owner=arg_l['user'])
        query_perms=query_tag.filter(perms__holder=arg_l['user'].holder,perms__perm_label='can_list')
        query= query_public | query_user | query_perms
    else:
        query=query_public


    #select only related objs if needed
    if arg_l['related'] is not None:
        query=query.select_related(arg_l['related'])

    return query.distinct()
