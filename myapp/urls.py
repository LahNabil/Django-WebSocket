from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('tasks',views.TaskItemViewSet, basename='task')

urlpatterns = [
     path('', include(router.urls))
]


"""
urlpatterns = [
    # Read - List all tasks
    path('', views.getData, name="tasks"),
    path('add/', views.addTask)
]
"""