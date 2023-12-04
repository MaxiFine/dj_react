from rest_framework import serializers
from .models import CustomUser



# User serializer
class UserSerializerClass(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 
                  'bio', 'avatar', 'email', 'is_active', 'created',
                  'updated']
        read_only_field = ['is_active']