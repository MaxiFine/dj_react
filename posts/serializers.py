# Serializing the Models for Posts

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# imports from apps
# from accounts.serializers import AbstractPostSerializer
from .models import Post
from accounts.models import CustomUser


# To be used to as a subclass for fields that will need the 
# following fields data: User as a subclass for the CustomUser
class AbstractPostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, 
                               format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)



# writing Post Serializer to serialize User Posts
class PostSerializer(AbstractPostSerializer):
    author = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), 
                                   slug_field='public_id')
    
    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")
        return value
    
    class Meta:
        model = Post
        # list fields that can be included in the request or response
        fields = ['id', 'author', 'body', 'edited',
                  'created', 'updated']
        read_only_fields = ['edited']



        