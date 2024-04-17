from django.shortcuts import render
from django.http import HttpResponse
from .send import mqsend, objMQSend
from .receive import mqreceive
# Create your views here.

def receive(request):
    headers,tags=mqreceive(queue='DC', delivery_tag=1, stop_tag='stop')
    response=''
    for i,tag in enumerate(tags):
        for k,v in headers[i].items():
                response+='{} : {} /'.format(k,v)
        response+= tag+'<br>'
    return HttpResponse(response)

def send(request,body):
    from filer.models import File
    files=File.objects.filter(_status=0)
    response=''
    for file in files:
        objMQSend(file,file.file.name)
        file._status=1
        file.save()
        response+=file.name+'<br>'
    return HttpResponse(response)
