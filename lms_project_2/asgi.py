"""
ASGI config for lms_project_2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application

from chat_module import routing as chat_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project_2.settings')
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(
                    chat_routing.websocket_urlpatterns
                )
            )
        )
    )
})

