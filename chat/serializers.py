from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import UserSerializer

class ConversationSerializer(serializers.ModelSerializer):
    initiator = UserSerializer()
    receiver = UserSerializer()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'start_time', 'last_message', 'unread_count']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(read=False).exclude(sender=request.user).count()
        return 0

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp', 'read']
        read_only_fields = ['id', 'sender', 'timestamp']