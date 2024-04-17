from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Column
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .serializers import ColumnSerializer
from django.core import serializers
from core.utils import get_code


class ColumnRestView(APIView):
    def get(self,request,uid,columnid): #,uid,columnid
        """
        get column info from dataset.
        """
        column=get_object_or_404(Column.objects.select_related('dataset'),id=columnid,dataset__datafile__uid=uid)
        if column.dataset.datafile.has_perm(request.user.holder,'can_read'):
            serializer = ColumnSerializer(column)
            return JsonResponse(serializer.data)
        return JsonResponse({'no permissions':'user is not allowed to read this dataset'}, status=401)

    def put(self,request,uid,columnid):
        column=get_object_or_404(Column.objects.select_related('dataset'),id=columnid,dataset__datafile__uid=uid)
        #import ipdb; ipdb.set_trace()
        if column.dataset.datafile.has_perm(request.user.holder,'can_edit'):
            data = JSONParser().parse(request)

            serializer = ColumnSerializer(column, data=data)
            #import ipdb; ipdb.set_trace()
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            #import ipdb; ipdb.set_trace()
            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({'no permissions':'user is not allowed to edit this dataset'}, status=401)
