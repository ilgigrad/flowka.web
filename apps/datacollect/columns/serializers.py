
from rest_framework import serializers
from core.utils import get_code

from .models import Column
import json

class ColumnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = ('id', 'rename','drop_column','target','alter','nan','category','outliers','alter_rule')

    def __init__(self,*args,**kwargs):
        super(ColumnSerializer,self).__init__(*args,**kwargs)
        #import ipdb; ipdb.set_trace()
        if kwargs['data'].get('alter') is None:
            self.initial_data['alter_rule']=''
            self.initial_data['alter']=get_code(self.instance.ALTERS,'unchanged')
        elif int(kwargs['data'].get('alter'))==get_code(self.instance.ALTERS,'unchanged'):
            self.initial_data['alter_rule']=''
        elif int(kwargs['data'].get('alter'))==get_code(self.instance.ALTERS,'splitize'):
            substrings=[int(x) for x in kwargs['data'].get('substrings',[])]
            self.initial_data['alter_rule']=json.dumps({'splitize':{'spliter':kwargs['data'].get('spliter',''),'substrings':substrings}})
        elif int(kwargs['data'].get('alter'))==get_code(self.instance.ALTERS,'timize'):
            timeselect=kwargs['data'].get('timeselect',[])
            self.initial_data['alter_rule']=json.dumps({'timize':{'dt_format':kwargs['data'].get('dt_format',''),'timeselect':timeselect}})
        elif int(kwargs['data'].get('alter'))==get_code(self.instance.ALTERS,'substrize'):
            substrings=kwargs['data'].get('substrings',[])
            self.initial_data['alter_rule']=json.dumps({'substrize':{'substrer':kwargs['data'].get('substrer',[]),'substrings':substrings}})
        elif int(kwargs['data'].get('alter'))==get_code(self.instance.ALTERS,'regexize'):
            self.initial_data['alter_rule']=json.dumps({'regexize':{'regex':kwargs['data'].get('regex','')}})
        if kwargs['data'].get('nan') is None:
            self.initial_data['nan_rule']=''
            self.initial_data['nan']=get_code(self.instance.NANS,'leave')
        if kwargs['data'].get('category') is None:
            self.initial_data['category']=get_code(self.instance.CATEGORIES,'keep')



    def update(self, instance, validated_data):
        #import ipdb; ipdb.set_trace()
        super(ColumnSerializer,self).update(instance, validated_data)
        return instance


    def validate_drop_column(self, value):
        """
        Check that the blog post is about Django.
        """
        if value in [True,False]:
            return value
        raise serializers.ValidationError("Drop_column is not Boolean")
