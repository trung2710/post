"""
ASGI config for post project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
# Asynchronous Server Gateway Interface
'''Giao diện cổng máy chủ không đồng bộ là quy ước gọi cho các máy chủ web
 để chuyển tiếp yêu cầu đến các ứng dụng và khung Python có khả năng không đồng bộ. 
Nó được xây dựng như một sự kế thừa cho Giao diện cổng máy chủ Web.'''
import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post.settings')
#khoi tao cac ung dung chi xu li cac yeu cau HTTP
django_asgi_app = get_asgi_application()

from a_rtchat import routing
#bo dinh tuyen co thee xu ly o cam web
application = ProtocolTypeRouter({
    "http":django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
    ),
})
