
from rest_framework import serializers
from message.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('is_visible','is_unread', 'received_at', 'is_read', 'tags', 'extra_tags', 'message')
