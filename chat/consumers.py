import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from chat.models import Conversation, Message
from urllib.parse import parse_qs

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
            
            # Get receiver_id from query params
            receiver_id = query_params.get('receiver_id', [None])[0]
            if not receiver_id:
                await self.close()
                return
            
            self.receiver = await self.get_user(int(receiver_id))
            
            # Get or create conversation
            self.conversation = await self.get_or_create_conversation(self.user, self.receiver)
            
            # Create consistent group name
            self.group_name = f"chat_{self.conversation.id}"
            
            await self.accept()
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            print(f"User {self.user.id} connected to conversation {self.conversation.id} with {self.receiver.id}")  # Debug
        except Exception as e:
            print(f"Error in connect: {e}")
            await self.close()

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            print(f"User {user_id} does not exist")
            raise

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            print(f"User {getattr(self, 'user', None)} disconnected")  # Debug
    
    async def receive(self, text_data):
        try:
            print(f"Received raw data: {text_data}")  # Debug
            text_data_json = json.loads(text_data)
            
            if 'message' not in text_data_json:
                await self.send(text_data=json.dumps({
                    'error': 'Message field is required'
                }))
                return

            message = text_data_json['message']
            print(f"User {self.user.id} sending message to conversation {self.conversation.id}")  # Debug
        
            # Save message to database
            await self.save_message(self.conversation, self.user, message)
        
            # Send message to group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username,
                    'sender_id': self.user.id,  # Added sender_id for debugging
                    'timestamp': str(await self.get_current_timestamp())
                }
            )
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON format',
                'details': str(e)
            }))
        except Exception as e:
            print(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            }))
        
    async def chat_message(self, event):
        print(f"Sending message to client: {event}")  # Debug
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],  # Added for debugging
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def get_or_create_conversation(self, user1, user2):
        # Ensure consistent ordering of users to prevent duplicate conversations
        if user1.id > user2.id:
            user1, user2 = user2, user1
            
        conversation, created = Conversation.objects.get_or_create(
            initiator=user1,
            receiver=user2
        )
        print(f"Conversation between {user1.id} and {user2.id}: {'created' if created else 'exists'} (ID: {conversation.id})")  # Debug
        return conversation

    @database_sync_to_async
    def save_message(self, conversation, sender, text):
        msg = Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=text
        )
        print(f"Message saved: ID {msg.id} in conversation {conversation.id}")  # Debug
        return msg

    @database_sync_to_async
    def get_current_timestamp(self):
        from django.utils import timezone
        return timezone.now()