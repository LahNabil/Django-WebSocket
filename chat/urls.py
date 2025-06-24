from django.urls import path
from . import views
# from .views import HomeView, RoomView


urlpatterns = [
    # path('', HomeView, name='home'),
    # path('<str:room_name>/<str:username>/', RoomView, name='room')
    path('chat/<str:room_name>/', views.chat_room, name='chat')
]


