from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mpcd.users.api.views import UserViewSet
from mpcd.dict.views import DefinitionViewSet, EntryViewSet, DictionaryViewSet, \
    ReferenceViewSet, TranslationViewSet, WordViewSet, LoanWordViewSet, CategoryViewSet
from mpcd.corpus.views import BibEntryViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


''' Dictionary API-Endpoints '''

router.register("lemmas", WordViewSet)
router.register("loanwords", LoanWordViewSet)
router.register("translations", TranslationViewSet)
# router.register("langs",LangViewSet)
router.register("categories", CategoryViewSet)
router.register("ref", ReferenceViewSet)
router.register("def", DefinitionViewSet)
router.register("entries", EntryViewSet, basename='entry')
router.register("dicts", DictionaryViewSet, basename='dict')

router.register("bib", BibEntryViewSet, basename='bib')


app_name = "api"
urlpatterns = router.urls
