import os
from channels.routing import ProtocolTypeRouter
from channels.asgi import get_channel_layer
from django.core.asgi import get_asgi_application
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "mpcd"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

'''
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
})
'''
channel_layer = get_channel_layer()
