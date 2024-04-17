#!/usr/bin/env python
import pika
from django.conf import settings
RMQ = settings.RABBITMQ

def mqsend(body=None, queue=None, headers=None ):
    credentials = pika.PlainCredentials(RMQ['USER'], RMQ['PASSWORD'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RMQ['SERVER'],port=RMQ['PORT'], virtual_host=RMQ['VHOST'], credentials=credentials))
    channel = connection.channel()
    queue = queue or RMQ['QUEUE']
    channel.queue_declare(queue = queue,
                          durable=True)

    if headers:
        properties=pika.BasicProperties(delivery_mode = 2,headers=headers,)
    else:
        properties=pika.BasicProperties(delivery_mode = 2,headers=headers,)

    channel.basic_publish(exchange='',
                          routing_key =  queue,
                          body=body,
                          properties=properties)

    connection.close()
    return body

def objMQSend(object,data):
    obj_kid='{}_id'.format(object.__class__.__name__)
    obj_kuid='{}_uid'.format(object.__class__.__name__)
    user_id=object.owner.id
    user_uid=object.owner.uid
    headers={obj_kid:object.id,obj_kuid:object.uid,'user_id':user_id,'user_uid':user_uid}
    mqsend(data,'DC',headers)
