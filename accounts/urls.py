# Creating Routes for the Viewset
from rest_framework import routers
from .views import UserViewSet


router = routers.SimpleRouter()

# register the user
router.register(r'user'/ UserViewSet, basename='user')
urlpatterns = [
    *router.urls,
]
