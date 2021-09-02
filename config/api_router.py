from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mpcd.users.api.views import UserViewSet
from mpcd.codex.views import CodexTokenViewSet
from mpcd.dict.views import EntryViewSet, DictionaryViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("codextokens", CodexTokenViewSet)
router.register("entries", EntryViewSet)
router.register("dicts", DictionaryViewSet)


app_name = "api"
urlpatterns = router.urls
