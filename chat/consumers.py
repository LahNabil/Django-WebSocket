import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from chat.models import Conversation, Message
from urllib.parse import parse_qs
import uuid

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        query_params = parse_qs(self.scope['query_string'].decode())
        token = query_params.get('token', [None])[0]
        
        if not token:
            await self.close()
            return

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            self.user = await self.get_user(user_id)
            
            receiver_id = query_params.get('receiver_id', [None])[0]
            if not receiver_id:
                await self.close()
                return
            
            self.receiver = await self.get_user(uuid.UUID(receiver_id))
            
            self.conversation = await self.get_or_create_conversation(self.user, self.receiver)
            self.group_name = f"chat_{self.conversation.id}"
            
            await self.accept()
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            
            # Mark previous messages as read when connecting
            await self.mark_messages_as_read(self.conversation, self.user)
            
        except Exception as e:
            print(f"Connection error: {str(e)}")
            await self.close()

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message')
            
            if not message:
                return await self.send_error("Message content is required")
            
            # Save message to database
            saved_message = await self.save_message(
                conversation=self.conversation,
                sender=self.user,
                text=message
            )
            
            # Send message to group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message_id': str(saved_message.id),
                    'message': message,
                    'sender_id': str(self.user.id),
                    'sender_username': self.user.username,
                    'timestamp': saved_message.timestamp.isoformat(),
                    'read': saved_message.read
                }
            )
            
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
        except Exception as e:
            await self.send_error(str(e))
    
    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message_id': event['message_id'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'message': event['message'],
            'timestamp': event['timestamp'],
            'read': event['read']
        }))

    @database_sync_to_async
    def get_or_create_conversation(self, user1, user2):
        # Sort users to ensure consistent conversation
        if user1.id > user2.id:
            user1, user2 = user2, user1
        conversation, _ = Conversation.objects.get_or_create(
            initiator=user1,
            receiver=user2
        )
        return conversation

    @database_sync_to_async
    def save_message(self, conversation, sender, text):
        return Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=text
        )

    @database_sync_to_async
    def mark_messages_as_read(self, conversation, user):
        other_user = conversation.initiator if user == conversation.receiver else conversation.receiver
        Message.objects.filter(
            conversation=conversation,
            sender=other_user,
            read=False
        ).update(read=True)