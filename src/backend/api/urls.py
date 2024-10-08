from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import LightSwitchViewSet, SocketSwitchViewSet

app_name='api'

router = DefaultRouter()
router.register(r'lightswitch', LightSwitchViewSet, basename='lightswitch')
router.register(r'socketswitch', SocketSwitchViewSet, basename='socketswitch')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]