from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/balance/<int:meter_number>/', consumers.PrepaidBalanceConsumer.as_asgi()),
    path('ws/consumption/<int:meter_number>/', consumers.ElectricityConsumptionConsumer.as_asgi()),
]