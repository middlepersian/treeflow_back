# rest/urls.py
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
# import views for corpus
from treeflow.rest.views.bibliography import BibEntryViewSet
from treeflow.rest.views.comment import CommentViewSet
from treeflow.rest.views.dependency import DependencyViewSet
from treeflow.rest.views.feature import FeatureViewSet
from treeflow.rest.views.pos import POSViewSet
from treeflow.rest.views.section import SectionViewSet
from treeflow.rest.views.text import TextViewSet
from treeflow.rest.views.token import TokenViewSet
# import views for dictionary
from treeflow.rest.views.lemma import LemmaViewSet
from treeflow.rest.views.sense import SenseViewSet



router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# corpus
router.register(r'bibliography', BibEntryViewSet, basename='bibliography-list')
router.register(r'comments', CommentViewSet, basename='comment-list')
router.register(r'dependencies', DependencyViewSet, basename='dependency-list')
router.register(r'features', FeatureViewSet, basename='feature-list')
router.register(r'pos', POSViewSet, basename='pos-list')
router.register(r'sections', SectionViewSet, basename='section-list')
router.register(r'texts', TextViewSet, basename='text-list')
router.register(r'tokens', TokenViewSet, basename='token-list')

# Custom URL pattern for accessing sections by identifier
# dictionary
router.register(r'lemmas', LemmaViewSet, basename='lemmas')
router.register(r'senses', SenseViewSet, basename='sense-list')


app_name = "treeflow.rest"

urlpatterns = [
    path('', include(router.urls)),
]