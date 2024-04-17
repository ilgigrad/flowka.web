
from rest_framework import serializers
from datacollect.models import DataSet
from .columns.models import Column
from filer.models import File

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('datafile','snippet', 'metadata')

    def create(self, validated_data):
        #import ipdb; ipdb.set_trace()
        file=validated_data.get('datafile')
        if file:
            file.status=File.FILE_STATUS.get_value('load')
            file.is_valid=True
            file.save()
            dataset=DataSet.objects.create(**validated_data)
            return dataset
        else:
            return None

    def update(self, instance, validated_data):
        #instance.snippet=validated_data.get('snippet',instance.snippet)
        #instance.metadata=validated_data.get('metadata',instance.metadata)
        instance.clean=validated_data.get('clean',instance.clean)


class TransformSerializer(serializers.ModelSerializer):
     class Meta:
         model = DataSet
         fields = ('transform')

class CleanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('clean')

    def update(self, instance, validated_data):
        instance.clean=validated_data.get('clean',instance.clean)
