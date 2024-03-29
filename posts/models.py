import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


# was expecting a public id but
# # Abstract Model Manager Definition
# class AbstractManager(models.Manager):
#     def get_object_by_public_id(self, public_id):
#         try:
#             isinstance = self.get(public_id)
#             return isinstance
#         except (ObjectDoesNotExist, ValueError, TypeError):
#             return Http404

# switched to use a primary key by the self.get method
# and not the public id
class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            # Assuming `public_id` is a field in your model
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404
    

# Abstract Model definition
class AbstractModels(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = AbstractManager()

    class Meta:
        abstract = True


# models for Post Using Abstractions
# Post manager
class PostManager(AbstractManager):
    pass


# Post class for user to make Posts
class Post(AbstractModels):
    author = models.ForeignKey(to="accounts.CustomUser", on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    
    objects = PostManager()

    def __str__(self):
        return f"{self.author.name}"
    
    class Meta:
        db_table = 'post'

        