from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from filer.models import File
from filer.serializers import DataFileSerializer
from rest_framework.views import APIView


class DataFileRestView(APIView):

    def get_file(self, uid):
        try:
            return File.objects.get(uid=uid)
        except File.DoesNotExist:
            raise Http404

    def get(self,request,uid):
        """
        return data within a dataset
        """
        file=self.get_file(uid)
        serializer = DataFileSerializer(file, many=False)
        return Response(serializer.data)
        #return JsonResponse(serializer.data)

    @csrf_exempt
    def post(self,request):
        #import ipdb; ipdb.set_trace()
        data=JSONParser().parse(request)
        serializer=DataFileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @csrf_exempt
    def put(self,request,uid):
        #import ipdb; ipdb.set_trace()
        file=self.get_file(uid)
        data = JSONParser().parse(request)
        serializer = DataFileSerializer(file, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors, status=400)
