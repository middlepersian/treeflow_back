import os
from django.core.asgi import get_asgi_application
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "mpcd"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django_application = get_asgi_application()
#channel_layer = get_channel_layer()
# Import websocket application here, so apps from django_application are loaded first
from config.websocket import websocket_application  # noqa isort:skip


async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")

