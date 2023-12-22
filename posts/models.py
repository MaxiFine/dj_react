import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404



# Abstract Model Manager Definition
class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            isinstance = self.get(public_id)
            return isinstance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
    

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


# Post Manager
class Post(AbstractModels):
    author = models.ForeignKey(to="accounts.CustomUser", on_delete=models.CASCADE)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    
    objects = PostManager()

    def __str__(self):
        return f"{self.author.name}"
    
    class Meta:
        db_table = 'post'

        