from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
            
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email']),
            password=password,
            **{k: v for k, v in validated_data.items() if k != 'email'}
        )
        return user