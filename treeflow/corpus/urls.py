from django.urls import include, path
from treeflow.corpus.views.update_token import update_token
from treeflow.corpus.views.sections import sections_view

app_name = "treeflow.corpus"
urlpatterns = [
    path('update_token/', update_token, name='update_token'),
    path('sections/', sections_view, name='sections_view'),
]
