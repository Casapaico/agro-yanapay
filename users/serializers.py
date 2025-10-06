from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'user_type_display', 'community', 'phone',
            'profile_picture', 'is_verified', 'date_joined', 'last_login'
        )
        read_only_fields = ('id', 'date_joined', 'last_login')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type', 'community', 'phone'
        )
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user