import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from chat.models import Conversation, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        token_param = [param.split('=') for param in query_string.split('&') if param.startswith('token=')]
        
        if not token_param:
            await self.close()
            return

        token = token_param[0][1]
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            self.user = await self.get_user(user_id)
            self.conversation_name = self.scope['url_route']['kwargs']['conversation_name']
            
            await self.accept()
            await self.channel_layer.group_add(
                self.conversation_name,
                self.channel_name
            )
        except Exception as e:
            print(e)
            await self.close()

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.conversation_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_id = text_data_json['receiver_id']
        
        receiver = await database_sync_to_async(User.objects.get)(id=receiver_id)
        conversation = await self.get_or_create_conversation(self.user, receiver)
        
        await self.save_message(conversation, self.user, message)
        
        await self.channel_layer.group_send(
            self.conversation_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': str(self.get_current_timestamp())
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def get_or_create_conversation(self, user1, user2):
        conversation, created = Conversation.objects.get_or_create(
            initiator=user1,
            receiver=user2
        )
        return conversation

    @database_sync_to_async
    def save_message(self, conversation, sender, text):
        Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=text
        )

    @database_sync_to_async
    def get_current_timestamp(self):
        from django.utils import timezone
        return timezone.now()