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
    

