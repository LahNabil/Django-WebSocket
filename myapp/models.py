from django.db import models
from django.conf import settings

# Create your models here.

class TaskItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks', null=True)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at'] # Order tasks by most recent first