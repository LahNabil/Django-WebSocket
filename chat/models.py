from django.db import models
from django.conf import settings
import uuid

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='convo_starter')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='convo_participant')
    start_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('initiator', 'receiver')

    def __str__(self):
        return f"Conversation between {self.initiator} and {self.receiver}"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_sender')
    text = models.TextField()  # Changed from CharField to TextField for longer messages
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Added read status

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f"Message from {self.sender} in {self.conversation}"
    
# class Message(models.Model):
#     receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages', null=True)
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages', null=True)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{str(self.content)} - {self.sender} --> {self.receiver}"


