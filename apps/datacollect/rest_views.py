from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from .models import DataSet
from .serializers import DataSetSerializer, TransformSerializer,  CleanSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


class DataSetRestView(APIView):

    def get(self,request,uid):
        """
        return data within a dataset
        """
        dataset=get_object_or_404(DataSet,datafile__uid=uid)
        serializer = DataSetSerializer(dataset, many=False)
        return Response(serializer.data)
        #return JsonResponse(serializer.data)

    #@csrf_exempt
    def post(self,request,uid):
        data=JSONParser().parse(request)
        serializer=DataSetSerializer(data=data)
        #serializer=DataSetSerializer(data=request.data)
        if serializer.is_valid():
            dataset=serializer.save()
            #import ipdb; ipdb.set_trace()
            if dataset is None:
                return JsonResponse(serializer.data, status=404)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    #@csrf_exempt
    def put(self,request,uid):
        dataset=get_object_or_404(DataSet,datafile__uid=uid)
        data = JSONParser().parse(request)
        serializer = DataSetSerializer(dataset, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


class TransformRestView(APIView):

    def get(self,request,uid):
        """
        return transformation logs within a dataset
        """
        dataset=get_object_or_404(DataSet,datafile__uid=uid)
        serializer = TransformSerializer(dataset, many=False)
        return Response(serializer.data)


class CleanRestView(APIView):

    @csrf_exempt
    def put(self,request,uid):

        dataset=get_object_or_404(DataSet,datafile__uid=uid)
        data = JSONParser().parse(request)
        serializer = CleanSerializer(dataset, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
