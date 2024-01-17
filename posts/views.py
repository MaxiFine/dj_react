from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, filters  # for Abstractviewsets

from rest_framework.response import Response
# internal imports 
# from accounts.views import AbstractViewSet 
from .models import Post
from .serializers import PostSerializer



# Abstract viewset to avoid DRY in PostSerializers
#  subclass the UserSerializer 
class AbstractViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    odering_fields = ['updated', 'created']
    ordering = ['-updated']
   

# Handling User Posts
class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get',)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    # returning objects methods
    def get_queryset(self):
        return Post.objects.all()
    
    # returning a single objects
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    # creating an object
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




