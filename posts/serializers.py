# Serializing the Models for Posts

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# imports from apps
# from accounts.serializers import AbstractPostSerializer
from .models import Post
from accounts.models import CustomUser
from accounts.serializers import UserSerializerClass
from .utils import AbstractSerializer



# writing Post Serializer to serialize User Posts
class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset= CustomUser.objects.all(), 
                                   slug_field='public_id')
    # print(author)
    
    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")
        return value
    
    # Using the ppublic_id to retrieve the user and serialize the user object
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = CustomUser.objects.get_object_by_public_id(
            rep['author']
        )
        rep['author'] = UserSerializerClass(author).data
        return rep
        
    
    class Meta:
        model = Post
        # list fields that can be included in the request or response
        fields = ['id', 'author', 'body', 'edited',
                  'created', 'updated']
        read_only_fields = ['edited']



        