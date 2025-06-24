from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from .models import TaskItem
from .serializers import TaskItemSerializer
from .permissions import IsOwner

class TaskItemViewSet(viewsets.ModelViewSet):
    serializer_class = TaskItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return TaskItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
    