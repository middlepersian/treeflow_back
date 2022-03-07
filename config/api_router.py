from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mpcd.users.api.views import UserViewSet

from mpcd.dict.views import DefinitionViewSet, EntryViewSet, DictionaryViewSet, \
    ReferenceViewSet, TranslationViewSet, WordViewSet, LoanWordViewSet, CategoryViewSet

from mpcd.corpus.views import AuthorViewSet
from mpcd.corpus.views import BibEntryViewSet
from mpcd.corpus.views import CodexViewSet, FolioViewSet, LineViewSet
from mpcd.corpus.views import CorpusViewSet, ResourceViewSet, TextViewSet, SentenceViewSet
from mpcd.corpus.views import EditionViewSet
from mpcd.corpus.views import TextSigleViewSet
from mpcd.corpus.views import  MorphologicalAnnotationViewSet, DependencyViewSet, TokenViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


''' Corpus API-Endpoints'''


router.register("author", AuthorViewSet)
router.register("bibliography", BibEntryViewSet)

router.register("codex", CodexViewSet)
router.register("folio", FolioViewSet)
router.register("line", LineViewSet)

router.register("corpus", CorpusViewSet)
router.register("resource", ResourceViewSet)
router.register("text", TextViewSet)

router.register("sentence", SentenceViewSet)
router.register("edition", EditionViewSet)
router.register("sigle", TextSigleViewSet)
router.register("morphological_annotation", MorphologicalAnnotationViewSet)
router.register("dependency", DependencyViewSet)
router.register("token", TokenViewSet, basename="token")


''' Dictionary API-Endpoints '''

router.register("dict", DictionaryViewSet, basename='dict')
router.register("entry", EntryViewSet, basename='entry')
router.register("lemma", WordViewSet)
router.register("loanword", LoanWordViewSet)
router.register("translation", TranslationViewSet)
# router.register("langs",LangViewSet)
router.register("category", CategoryViewSet)
router.register("reference", ReferenceViewSet)
router.register("definition", DefinitionViewSet)


app_name = "api"
urlpatterns = router.urls
