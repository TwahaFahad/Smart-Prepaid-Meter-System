from rest_framework import viewsets
from api.serializers import LightSwitchSerializer, SocketSwitchSerializer

from balances.models import LightSwitch, SocketSwitch


class LightSwitchViewSet(viewsets.ModelViewSet):
    queryset = LightSwitch.objects.all()
    serializer_class = LightSwitchSerializer
    

class SocketSwitchViewSet(viewsets.ModelViewSet):
    queryset = SocketSwitch.objects.all()
    serializer_class = SocketSwitchSerializer
    