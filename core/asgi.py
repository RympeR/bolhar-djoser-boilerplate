import os
import django
# from channels.http import AsgiHandler
# from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# django.setup()
django.setup()

application = get_asgi_application()
# application = ProtocolTypeRouter({