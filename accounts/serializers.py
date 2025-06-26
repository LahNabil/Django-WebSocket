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
        # Set is_active=True by default if not specified
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
            
        # Extract password separately
        password = validated_data.pop('password')
        
        # Create user using the manager's create_user method
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email']),  # Fallback to email if username not provided
            password=password,
            **{k: v for k, v in validated_data.items() if k != 'email'}  # Exclude email to avoid duplication
        )
        return user