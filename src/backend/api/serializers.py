from rest_framework import serializers

from balances.models import SocketSwitch, LightSwitch


class SocketSwitchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SocketSwitch
        fields = '__all__'


class LightSwitchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LightSwitch
        fields = '__all__'
