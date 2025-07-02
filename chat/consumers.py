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
            self.user_group_name = f"chat_user_{self.user.id}"

            await self.accept()
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.channel_layer.group_add(self.user_group_name, self.channel_name)

            # Mark messages as read on connection
            await self.mark_messages_as_read(self.conversation, self.user)

        except Exception as e:
            print(f"Connection error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            if data.get('type') == 'read_receipt':
                message_id = data.get('message_id')
                if message_id:
                    try:
                        message_uuid = uuid.UUID(message_id)
                        message = await self.mark_single_message_as_read(message_uuid)
                        if message:
                            print("Before notifying user...........")
                            await self.channel_layer.group_send(
                                f"chat_user_{message.sender.id}",
                                {
                                    'type': 'read_receipt',
                                    'message_id': str(message.id)
                                }
                            )
                            print("Successfully notified...............")
                    except (ValueError, AttributeError) as e:
                        print(f"Invalid message ID: {str(e)}")
                        await self.send_error("Invalid message ID")
                    return

            message = data.get('message')
            if not message:
                return await self.send_error("Message content is required")

            saved_message = await self.save_message(
                conversation=self.conversation,
                sender=self.user,
                text=message
            )

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
            print("Error while sending message")
            await self.send_error("Invalid JSON format")
        except Exception as e:
            print("unknown error", str(e))
            await self.send_error(str(e))

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

    async def read_receipt(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'message_id': event['message_id']
        }))

    async def send_error(self, message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_or_create_conversation(self, user1, user2):
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

    @database_sync_to_async
    def mark_single_message_as_read(self, message_id):
        try:
            message = Message.objects.select_related('sender').get(id=message_id)
            if not message.read:
                message.read = True
                message.save(update_fields=['read'])
            return message
        except Message.DoesNotExist:
            return None