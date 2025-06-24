from django.urls import path
from . import views
# from .views import HomeView, RoomView


urlpatterns = [
    path('chat/<str:room_name>/', views.chat_room, name='chat')
]


