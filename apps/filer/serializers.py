
from rest_framework import serializers
from filer.models import File

class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('subjects',)

    def create(self, validated_data):
        #import ipdb; ipdb.set_trace()
        return DataSet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_valid=validated_data.get('is_valid',instance.is_valid)
        instance.save()
        return instance
