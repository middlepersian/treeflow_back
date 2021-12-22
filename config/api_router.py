from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mpcd.users.api.views import UserViewSet

from mpcd.dict.views import DefinitionViewSet, EntryViewSet, DictionaryViewSet, \
    ReferenceViewSet, TranslationViewSet, WordViewSet, LoanWordViewSet, CategoryViewSet

from mpcd.corpus.views import AuthorViewSet
from mpcd.corpus.views import BibEntryViewSet
from mpcd.corpus.views import CodexViewSet
from mpcd.corpus.views import CorpusViewSet, ResourceViewSet, TextViewSet, SentenceViewSet
from mpcd.corpus.views import EditionViewSet
from mpcd.corpus.views import TextSigleViewSet
from mpcd.corpus.views import FeatureValueViewSet, FeatureViewSet, \
    MorphologicalAnnotationViewSet, DependencyViewSet, SyntacticAnnotationViewSet, \
    PosViewSet, TokenViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


''' Corpus API-Endpoints'''


router.register("author", AuthorViewSet)
router.register("bibliography", BibEntryViewSet)
router.register("codex", CodexViewSet)
router.register("corpus", CorpusViewSet)
router.register("resource", ResourceViewSet)
router.register("text", TextViewSet)
router.register("sentence", SentenceViewSet)
router.register("edition", EditionViewSet)
router.register("sigle", TextSigleViewSet)
router.register("fearure_value", FeatureValueViewSet)
router.register("feature", FeatureViewSet)
router.register("morphological_annotation", MorphologicalAnnotationViewSet)
router.register("dependency", DependencyViewSet)
router.register("syntactic_annotation", SyntacticAnnotationViewSet)
router.register("pos", PosViewSet)
router.register("token", TokenViewSet)


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


app_name = "api"
urlpatterns = router.urls
