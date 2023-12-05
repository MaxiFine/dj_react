# Creating Routes for the Viewset
from rest_framework import routers
from .views import UserViewSet, RegisterViewSet, LoginViewSet


router = routers.SimpleRouter()

# register the user
router.register(r'user', UserViewSet, basename='user')
router.register(r'register', RegisterViewSet, basename='user-registration')
router.register(r'login', LoginViewSet, basename='login')
urlpatterns = [
    *router.urls,
]
