from rest_framework import routers
from django.urls import path, include

from .views import PostViewSet

# using Router
router = routers.SimpleRouter()

router.register(r'post', PostViewSet, basename='post')


urlpatterns = [
    *router.urls,
]
