from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .serializers import UserSerializerClass
from .models import CustomUser



class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = [AllowAny]
    serializer_class = UserSerializerClass

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.exclude(is_superuser=True)
    
    def get_object(self):
        obj = CustomUser.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj