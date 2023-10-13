"""
ASGI config for Interface project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# import project.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Interface.settings')

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket':AuthMiddlewareStack(
#         URLRouter(
#             project.routing.websocket_urlpatterns
#         )
#     )
# })
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Interface.settings")

application = get_asgi_application()