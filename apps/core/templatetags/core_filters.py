from django.template import Library
from core.utils import toInt
register = Library()

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

@register.filter(name='dict')
def get_from_dict(dict, key):
    #import ipdb; ipdb.set_trace()
    return dict.get(key,None)

@register.filter(name='list')
def list(value, arg):
    return value[toInt(arg)]


@register.filter(name='sub')
def sub(value, arg):
    if isinstance(value,str):
        value=int(value)
    if isinstance(arg,str):
        arg=int(arg)
    return value - arg

@register.filter(name='int')
def to_int(value):
    if isinstance(value,str) or isinstance(value,float):
        return int(value)
    return value

@register.filter(name='multi')
def multi(value, arg):
    if isinstance(value,str):
        value=int(value)
    if isinstance(arg,str):
        arg=int(arg)
    return value * arg


@register.filter(name='divide')
def divide(value, arg):
    if isinstance(value,str):
        int(value)
    if isinstance(arg,str):
        arg=int(arg)
    if arg==0:
        return 0
    return value / arg

@register.filter
def as_id(value):
    return value.replace(",","")
