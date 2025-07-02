from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation_messages(request, receiver_id):
    try:
        # Convert receiver_id string to UUID object
        receiver_uuid = uuid.UUID(receiver_id)
        receiver = get_object_or_404(User, id=receiver_uuid)
        
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
    except ValueError:
        return Response({'error': 'Invalid receiver ID format'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_counts(request):
    try:
        user = request.user
        conversations = Conversation.objects.filter(
            models.Q(initiator=user) | models.Q(receiver=user)
        )

        result = []
        for conv in conversations:
            other = conv.receiver if conv.initiator == user else conv.initiator
            unread_count = Message.objects.filter(
                conversation=conv,
                sender=other,
                read=False
            ).count()
            result.append({
                'id': str(other.id),
                'name': other.username,
                'email': other.email,
                'unread_count': unread_count
            })

        return Response(result)

    except Exception as e:
        print("ERROR in unread_counts:", str(e))
        return Response({'error': str(e)}, status=400)



