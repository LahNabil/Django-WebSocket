
# import os
# # from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from chat.routing import wsPattern 
# from chat.middleware import JWTAuthMiddleware 

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

# http_response_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": http_response_app,
#     # "websocket": URLRouter(wsPattern)
#     "websocket": JWTAuthMiddleware(
#         URLRouter(
#             wsPattern
#             # chat.routing.websocket_urlpatterns
#         )
#     ),
# })

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

