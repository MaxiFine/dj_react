from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings  # u login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login

from .models import CustomUser

from posts.serializers import AbstractPostSerializer



# User serializer
class UserSerializerClass(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 
                  'email', 'is_active', 'created',
                  'updated']
        read_only_field = ['is_active']


# User Registration Serializer
class RegistrationSerializer(UserSerializerClass):
    """
    Registration serializer for requests and user creation
    """
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email',
                'username', 'first_name', 'last_name', 'password'
                ]
    # let's create the user
    def create(self, validation_data):
        # Use the create_user to create user4
        return CustomUser.objects.create_user(**validation_data)
    

#Login Serializer
class UserLoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['user'] = UserSerializerClass(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


# Joining the Post with Users
