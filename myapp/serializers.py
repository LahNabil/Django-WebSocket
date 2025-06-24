from rest_framework import serializers
from .models import TaskItem

class TaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskItem
        fields = ['id', 'title', 'completed', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']