from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation_messages(request, receiver_id):
    try:
        receiver = get_object_or_404(User, id=receiver_id)
        
        # Find the conversation between current user and receiver
        conversation = Conversation.objects.filter(
            models.Q(initiator=request.user, receiver=receiver) |
            models.Q(initiator=receiver, receiver=request.user)
        ).first()
        
        if not conversation:
            return Response([])
            
        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)