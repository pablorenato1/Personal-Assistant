from django.urls import re_path, path

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from project.consumers import InterfaceConsumer, PersonalAssistantLog

websocket_urlpatterns = [
    re_path("ws/update/", InterfaceConsumer.as_asgi()),
    re_path('ws/voiceOutput/', PersonalAssistantLog.as_asgi())
]

