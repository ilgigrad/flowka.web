from django.db import models
from filer.models import File
from django.utils.translation import ugettext_lazy as _
import json
from core.utils import toStr
from django.utils.text import slugify
import numpy as np
# Create your models here.


class DataSet(models.Model):
    datafile = models.ForeignKey(File,models.CASCADE,verbose_name=_('datafile'),null=True)
    snippet=models.TextField(blank=True, null=True)
    metadata=models.TextField(blank=True, null=True)
    transform=models.TextField(blank=True, null=True)
    clean=models.TextField(blank=True, null=True)


    META={
        'column':_('label or column name'),
        'type':_('data type (string, integer, float, date, time...)'),
        'count':_('Total number of values in the dataset'),
        'valid':_('Number of valid values in the dataset'),
        'distinct':_('number of distinct values in the dataset. A number of distinct values equal to count values and string data types could be a name or an identifier and should be removed'),
        'nan':_('Not a Number, none, null or missing values. rules avoiding nans have to be set. If not, Rows or columns with Nans need to be removed'),
        'min':_('minimum value'),
        'max':_('maximum value'),
        'maxlen':_('maximum length of the values for that label'),
        'minlen':_('minimum length of the values for that label'),
        'mean':_('average value for that label; Mean does not apply to objects or strings'),
        'stddev':_('Standard Deviation;  measure of the variation or the dispersion between the values'),
        'q10':_('first decile or 10th percentile; it is equal to the value below which 10% of the observations may be found; data below this first decile may be consider as outiers'),
        'q25':_('first quartile or 25th percentile; it is equal to the value below which 25% of the observations may be found'),
        'q50':_('median or 50th percentile; it is equal to the value below which 50% of the observations may be found'),
        'q75':_('third quartile or 75th percentile; it is equal to the value below which 75% of the observations may be found'),
        'q90':_('last decile or 90th percentile; it is equal to the value below which 90% of the observations may be found; data above the last decile may be consider as outiers'),
        }


    def __init__(self,*args,**kwargs):
        self.keys=None
        super(DataSet,self).__init__(*args,**kwargs)
        self.templatize()

    def save(self,init=False,*args,**kwargs):
        #import ipdb; ipdb.set_trace()
        if self.keys:
            self.get_drops()
            self.get_target()
            self.transform=self.serialize_columns()
        super(DataSet,self).save(*args,**kwargs)

    def templatize(self):
        """
            prepare info for template
        """
        from core.utils import dict_invert
        self.meta=dict_invert(json.loads(self.metadata))
        self.keys=list(self.meta.keys())
        self.clean_rows,self.clean_cols=self.get_data(self.clean,self.keys)
        self.meta_rows,self.meta_cols=self.get_data(self.meta,self.keys,transpose=True)
        self.origin_rows,self.origin_cols=self.get_data(self.snippet,self.keys)
        self.init_columns(self.keys)
        self.transform=self.serialize_columns()
        self.set_origin_cols_id()
        self.get_drops()
        self.get_target()
        self.get_metadesc()
        self.set_invalid_alert()
        self.set_nans_alert()
        self.set_id_alert()


    def get_data(self,data,keys,transpose=False):
        if isinstance(data,str):
            asdict=json.loads(data)
        else:
            asdict=data or {}

        if len(asdict)==0:
            return [],[]

        aslist=[]

        if transpose:
            heads=['column']+list(list(asdict.values())[0].keys())
            for key in keys:
                aslist.append([key]+list(asdict[key].values()))
        else:
            heads=['column']+keys
            for adkey,values in asdict.items():
                aslist.append([adkey]+[values[key] for key in keys])

        l=lambda x : len(toStr(x) or '')+2#get the size of a cell in the dataset
        lengths=list(map(lambda x : list(map(l,x)),aslist+[heads]))#for each column, get the max length
        max=np.amax(lengths,axis=0)
        sizes=[4,6,8,10,12,14,18,20]
        g=lambda chars :min(sizes, key=lambda x:abs(x-chars)) # get maximum between maxlength of the column and its title/name and make of list of distances of maxlength to sizes value
        widths=list(map(g,max)) #search the index of the minimal distance and report it to sizes list -> gives the size value closest to maxlength
        # put the size in the info headers
        columns=[{'head':heads[i],'width':widths[i], 'slug':slugify(heads[i])} for i in range(len(heads))]
        columns[0]['index']=True
        return aslist, columns


    def init_columns(self,keys):
        for key in keys:
            self.column_set.get_or_create(initial=key)

    def serialize_columns(self):
        from django.core import serializers
        return(serializers.serialize('json',list(self.column_set.all())))

    def deserialize_columns(self,data):
        self.column_set.all().delete()
        from django.core import serializers
        columns=serializers.deserialize('json',data,ignorenonexistent=True)
        for column in columns:
            column.save()

    def set_origin_cols_id(self):
        for c in self.origin_cols[1:]:
            c['id']=self.column_set.get(slug=c['slug']).id

    @property
    def max_snippet_width(self):
        return str(sum(item['width'] for item in self.origin_cols)).replace(',','')

    @property
    def max_meta_width(self):
        return str(sum(item['width'] for item in self.meta_cols)).replace(',','')

    @property
    def max_clean_width(self):
        return str(sum(item['width'] for item in self.clean_cols)).replace(',','')

    def get_drops(self):
        drops= [c.id for c in self.column_set.filter(drop_column=True)]
        for col in self.origin_cols:
            col['drop']= col.get('id',None) in drops
        return drops

    def get_target(self):
        target=self.column_set.filter(target=True).first()
        if target:
            target=target.id
        for col in self.origin_cols:
            col['target']= col.get('id',0) == target
        return target

    def set_id_alert(self):
        for col in self.origin_cols[1:]:
                col['id_alert']= self.meta[col['head']]['distinct']==self.meta[col['head']]['count']

    def set_nans_alert(self):
        for col in self.origin_cols[1:]:
            col['nans_alert']= self.meta[col['head']]['nan']>0

    def set_invalid_alert(self):
        for col in self.origin_cols[1:]:
            col['invalid_alert']= self.meta[col['head']]['valid']*3 <self.meta[col['head']]['count']

    def get_metadesc(self):
        for item in self.meta_cols:
            item['desc']=self.META[item['slug']]

    @property
    def counts(self):
        i=list(col['head'] for col in self.meta_cols).index('count')
        return max(row[i] for row in self.meta_rows)



#import datacollect.signals
