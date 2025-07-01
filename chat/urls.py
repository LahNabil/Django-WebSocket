from django.urls import path
from . import views
# from .views import HomeView, RoomView


urlpatterns = [
    path('messages/<str:receiver_id>/', views.get_conversation_messages, name='get_messages'),
]


