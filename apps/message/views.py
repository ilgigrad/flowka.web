from django.shortcuts import  redirect, get_object_or_404,render_to_response
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.generic import View
from message.models import Message
from django.template.response import TemplateResponse
from message.serializers import MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from core.utils import paginator

# class MessageListView(View):
#
#     context={}
#
#     def post(self,request):
#         return TemplateResponse(request,'message/message.html', self.context)
#
#     def get(self, request):
#         messages=Message.objects.read_or_last(request.user,max=25)
#         self.context={'posts':messages}
#         return TemplateResponse(request,'message/post.html', self.context)

class MessageListSerializer(APIView):

    def get(self,request):
        """
        List unread messages.
        """
        page=request.GET.get('page')
        messages=Message.objects.read_or_last(request.user,max=200)
        messages, paginate = paginator(messages,100,page)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
        #return JsonResponse(serializer.data)
