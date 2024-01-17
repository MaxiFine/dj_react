from rest_framework import routers
from django.urls import path, include

from .views import PostViewSet

# using Router
router = routers.SimpleRouter()
router.register(r'post', PostViewSet, basename='post')

# chat suggested this to fix the circular import error
urlpatterns = [
    path('api/', include(router.urls)),
]
