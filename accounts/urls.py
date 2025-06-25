from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('users/', views.get_all_users),
]