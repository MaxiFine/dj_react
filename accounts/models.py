import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


# Abracting the CustomUser
from posts.models import AbstractManager, AbstractModels
# Try this

# import  django
# django.setup()

# from posts.models import AbstractManager, AbstractModels


# # Abstract Model Manager Definition
# class AbstractManager(models.Model):
#     def get_object_by_public_id(self, public_id):
#         try:
#             isinstance = self.get(public_id)
#             return isinstance
#         except (ObjectDoesNotExist, ValueError, TypeError):
#             return Http404
    

# # Abstract Model definition
# class AbstractModels(models.Model):
#     public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     # objects = AbstractManager()

#     class Meta:
#         abstract = True




# creating the usermanager
class CustomUserManager(BaseUserManager, AbstractManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
    def create_user(self, username, email, password=None, **kwargs):
        """Create a user and return with email, username
            and password. """
        if username is None:
            raise TypeError('username must be set')
        if email is None:
            raise TypeError("User must have an email address")
        if password is None:
            raise TypeError("User must set Password")
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self, username, email, password=None, **kwargs):
        """
        Create and return a `User` with superuser (admin)
        permissions.
        """
        if username is None:
            raise TypeError('username must be set')
        if email is None:
            raise TypeError("User must have an email address")
        if password is None:
            raise TypeError("User must set Password")
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# User Model
class CustomUser(AbstractModels, AbstractBaseUser, PermissionsMixin):
    # removed to implement the abstract CustomUser in Posts models
    public_id = models.UUIDField(db_index=True, unique=True, 
                                 default=uuid.uuid4, 
                                 editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # removed for the CustomUser abstraction for Post model
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 




