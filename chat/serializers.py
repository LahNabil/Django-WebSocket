from rest_framework import serializers
from .models import Message
from accounts.serializers import UserSerializer  # Assuming you have this

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp']
        read_only_fields = ['id', 'timestamp']