from django.shortcuts import render
from rest_framework.decorators import api_view
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status 
from .models import User
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Create your views here.

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # is_active=True sera appliqué automatiquement
        return Response({
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "message": "Compte créé avec succès"
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)
    if user is not None:
        # Générer les tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Login successful"
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer_class = UserSerializer(users, many=True)
    return Response(serializer_class.data, status=status.HTTP_200_OK)
    



