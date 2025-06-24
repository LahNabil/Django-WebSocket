from django.db import models
from django.conf import settings

class Conversation(models.Model):
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='convo_starter', null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='convo_participant', null=True)
    start_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('initiator', 'receiver')

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_sender', null=True)
    text = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
# class Message(models.Model):
#     receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages', null=True)
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages', null=True)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{str(self.content)} - {self.sender} --> {self.receiver}"


