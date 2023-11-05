from django.urls import include, path
from treeflow.corpus.views.update_token import update_token
from treeflow.corpus.views.sections import sections_view
from treeflow.corpus.views.ud_editor import ud_editor

app_name = "treeflow.corpus"
urlpatterns = [
    path('update_token/', update_token, name='update_token'),
    path('sections/', sections_view, name='sections_view'),
    path('ud-editor/<uuid:section_id>/', ud_editor, name='ud_editor'), 
]