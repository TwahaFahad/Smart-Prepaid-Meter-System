"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from sockets.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

prepaid_asgi = get_asgi_application()


application = ProtocolTypeRouter({
    "http": prepaid_asgi,
    "websocket": URLRouter(websocket_urlpatterns),
    "https": prepaid_asgi,
    # Just HTTP for now. (We can add other protocols later.)
})

