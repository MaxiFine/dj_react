
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, views

# for user registration
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings 

from .serializers import UserSerializerClass, RegistrationSerializer, UserLoginSerializer
from .models import CustomUser


# Users Serializer to list all Users
class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializerClass

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.exclude(is_superuser=True)
    
    def get_object(self):
        obj = CustomUser.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    

# Registration Viewset to register new Users
class RegisterViewSet(viewsets.ViewSet):
    serializer_classes = RegistrationSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_classes(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
            }, status=status.HTTP_201_CREATED)
    

# # Login viewSet for users to logina
# class LoginViewSet(views.APIView):
#     # items needed to initiate user login
#     permission_classes = (AllowAny,)
#     #htttp_method_names = ['post']

#     def post(self, request, *args, **kwatgs):
#         serializer = UserLoginSerializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             raise InvalidToken(e.args[0])
#         refresh = RefreshToken.for_user(serializer.user)
#         data = {
#             'user': UserSerializerClass(serializer.user).data,
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         }
#         if api_settings.UPDATE_LAST_LOGIN:
#             update_last_login(None, serializer.user)
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class LoginViewSet(viewsets.ViewSet):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


